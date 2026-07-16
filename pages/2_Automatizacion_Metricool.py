import os
import re
import base64
from datetime import date, datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from html2image import Html2Image
from PIL import Image

from config import DATA_DIR, OUTPUT_DIR, FOTOS_DIR, LOGOS_DIR
from Descarga_fotos_propiedades import process_and_save_image
from google_drive_manager import get_drive_service, upload_image_to_drive, get_or_create_folder
import plantillas_carruseles_inmobiliarias
from main import procesar_fila_a_payload
from utils import formatear_atributo

# ── Variables de entorno ──────────────────────────────────────────────
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ── Constantes y mapeos ──────────────────────────────────────────────
PLANTILLAS_DISPONIBLES = {
    "Arquetipo A: Arquitectónico Minimalista": plantillas_carruseles_inmobiliarias.disenio_landscape_5fotos,
    "Arquetipo C: Bloque Corporativo": plantillas_carruseles_inmobiliarias.disenio_corporativo_5fotos,
    "Arquetipo C: Bloque Corporativo Claro": plantillas_carruseles_inmobiliarias.disenio_corporativo_claro_5fotos,
    "Arquetipo D: Dinámico Alternado (8 Fotos)": plantillas_carruseles_inmobiliarias.disenio_dinamico_alternado_5fotos,
}

MAPA_SLIDES_POR_PLANTILLA = {}

MAPA_OPERACION = {"sale": "Venta", "rent": "Renta"}

MAPA_EMOJI = {
    "condominio": "🏘️", "casa": "🏠", "departamento": "🏬",
    "apartment": "🏬", "terreno": "🏗️", "land": "🏗️",
    "lote": "🏗️", "oficina": "🏢", "local": "🏪",
}

MAPA_DIAS_NUM = {
    "Lunes": 0, "Martes": 1, "Miércoles": 2,
    "Jueves": 3, "Viernes": 4, "Sábado": 5, "Domingo": 6,
}

HORARIOS_DISPONIBLES = [
    "08:00", "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00",
]

# Columnas exactas del CSV de Metricool
COLUMNAS_METRICOOL = [
    "Text", "Date", "Time", "Draft", "Facebook", "Twitter/X", "LinkedIn",
    "GBP", "Instagram", "Pinterest", "TikTok", "Youtube", "Threads",
    "Bluesky", "Picture Url 1", "Picture Url 2", "Picture Url 3",
    "Picture Url 4", "Picture Url 5", "Picture Url 6", "Picture Url 7",
    "Picture Url 8", "Picture Url 9", "Picture Url 10",
    "Alt text picture 1", "Alt text picture 2", "Alt text picture 3",
    "Alt text picture 4", "Alt text picture 5", "Alt text picture 6",
    "Alt text picture 7", "Alt text picture 8", "Alt text picture 9",
    "Alt text picture 10", "Document title", "Shortener",
    "Video Thumbnail Url", "Video Cover Frame", "Twitter/X Can reply",
    "Twitter/X Type", "Twitter/X Poll Duration minutes",
    "Twitter/X Poll Option 1", "Twitter/X Poll Option 2",
    "Twitter/X Poll Option 3", "Twitter/X Poll Option 4",
    "Pinterest Board", "Pinterest Pin Title", "Pinterest Pin Link",
    "Pinterest Pin New Format", "Instagram Post Type",
    "Instagram Show Reel On Feed", "Youtube Video Title",
    "Youtube Video Type", "Youtube Video Privacy",
    "Youtube video for kids", "Youtube Video Category",
    "Youtube Video Tags", "Youtube playlist", "GBP Post Type",
    "Facebook Post Type", "Facebook Title", "First Comment Text",
    "TikTok Title", "TikTok disable comments", "TikTok disable duet",
    "TikTok disable stitch", "TikTok Post Privacy",
    "TikTok Branded Content", "TikTok Your Brand",
    "TikTok Auto Add Music", "TikTok Photo Cover Index",
    "TikTok musicId", "TikTok music title", "TikTok music author",
    "TikTok music previewUrl", "TikTok music thumbnailUrl",
    "TikTok music soundVolume", "TikTok music originalVolume",
    "TikTok music startMillis", "TikTok music endMillis",
    "TikTok is AI generated content", "LinkedIn Type",
    "LinkedIn Poll Question", "LinkedIn Poll Option 1",
    "LinkedIn Poll Option 2", "LinkedIn Poll Option 3",
    "LinkedIn Poll Option 4", "LinkedIn Poll Duration",
    "LinkedIn Show link preview", "LinkedIn Images as Carousel",
    "Threads Reply Control", "Threads Is Spoiler",
    "Threads Post Type", "Brand Name",
]


# =====================================================================
# FUNCIONES PURAS (sin dependencia de Streamlit)
# =====================================================================
def local_image_to_base64(filepath):
    """Convierte una imagen local a base64 data URI."""
    path = Path(filepath)
    if not path.exists():
        return ""
    try:
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        ext = path.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""


# formatear_atributo importado desde utils.py


def procesar_fila_a_payload_local(row):
    """Convierte una fila de Pandas en datos_propiedad usando fotos locales."""
    internal_id = str(row["InternalId"]).strip()
    if internal_id == "nan":
        return None, None, None, None

    company_raw = str(row.get("Company: Name", "Inmobiliaria")).strip()
    if company_raw.lower() == "nan":
        company_raw = "Inmobiliaria"
    company_clean = re.sub(r"[^A-Za-z0-9]+", "_", company_raw).strip("_")

    ruta_logo = LOGOS_DIR / f"{company_raw}_imagotipo_colab_negro.png"
    logo_b64 = local_image_to_base64(ruta_logo)

    property_folder = FOTOS_DIR / company_clean / internal_id

    def _foto(indice, total):
        return local_image_to_base64(property_folder / f"{internal_id}-photo-{indice+1:02d}-de-{total:02d}.jpg")

    pictures_raw = str(row.get("Pictures", ""))
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos = len(urls)

    def _clean(val, default=""):
        v = str(val).strip()
        return default if v.lower() == "nan" else v

    calle = _clean(row.get("Address: Street", "")).split(",")[0].strip()
    colonia = _clean(row.get("Address: Neighborhood: Name", ""))
    estado = _clean(row.get("Address: State: Name", ""))
    colonia_estado = f"{colonia}, {estado}".strip(", ")

    tipo = _clean(row.get("Type", ""))
    operacion = _clean(row.get("Listing: Operation", "")).lower()
    operacion = MAPA_OPERACION.get(operacion, operacion.capitalize() if operacion else "")
    tipo_operacion = " en ".join(filter(None, [tipo, operacion]))

    precio_crudo = str(row.get("Listing: Price: Price", "0")).strip()
    moneda = _clean(row.get("Listing: Price: Currency", "mxn"), "mxn").lower()
    precio_limpio = precio_crudo.replace(",", "").replace("$", "").replace(" ", "")
    try:
        precio = f"${float(precio_limpio):,.2f} {moneda}"
    except (ValueError, TypeError):
        precio = precio_crudo if precio_crudo.lower() != "nan" else ""

    attr_config = [
        (row.get("Attributes: Suites", ""), ("HABITACIÓN", "HABITACIONES")),
        (row.get("Attributes: Bathrooms", ""), ("BAÑO", "BAÑOS")),
        (row.get("Attributes: Parkings", ""), ("ESTACIONAMIENTO", "ESTACIONAMIENTOS")),
        (row.get("Attributes: TotalSurface", ""), "m² TOTALES"),
    ]
    atributos = "".join(f"<div>{a}</div>" for v, s in attr_config if (a := formatear_atributo(v, s)))

    datos_propiedad = {
        **{f"img{i+1}": _foto(i, total_fotos) for i in range(10)},
        "logo": logo_b64,
        "tipo_operacion": tipo_operacion,
        "precio": precio,
        "colonia_estado": colonia_estado,
        "calle": calle,
        "atributos_html": atributos,
    }
    return datos_propiedad, internal_id, company_clean, company_raw


def generar_copy_propiedad(datos_propiedad, api_key, modelo_seleccionado):
    """Genera texto de beneficio (1-2 líneas) usando OpenRouter."""
    if not api_key:
        return "Una excelente oportunidad que no puedes dejar pasar por su gran ubicación y espacios."

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    system_msg = (
        "Actúa como un experto copywriter inmobiliario. "
        "Genera un texto persuasivo muy breve (máximo 1 o 2 líneas) destacando "
        "el PRINCIPAL beneficio de esta propiedad. "
        "IMPORTANTE: NO incluyas saludos ni despedidas. NO uses emojis. "
        "NO uses hashtags. Ve directo al grano."
    )
    contexto = (
        f"Tipo: {datos_propiedad.get('tipo_operacion', 'N/A')}. "
        f"Precio: {datos_propiedad.get('precio', 'N/A')}. "
        f"Ubicación: {datos_propiedad.get('colonia_estado', 'N/A')}. "
        f"Calle: {datos_propiedad.get('calle', 'N/A')}. "
        f"Atributos: {datos_propiedad.get('atributos_html', '')}"
    )
    try:
        response = client.chat.completions.create(
            model=modelo_seleccionado,
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": contexto}],
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Una excelente oportunidad que no puedes dejar pasar por su gran ubicación y espacios."


def calcular_fechas_publicacion(fecha_inicio, dias_semana_permitidos, total_posts):
    """
    Función pura: calcula fechas de publicación distribuyendo slots sobre días permitidos.

    Args:
        fecha_inicio: Objeto date con la fecha de inicio.
        dias_semana_permitidos: Lista de strings (ej. ['Lunes', 'Miércoles', 'Viernes']).
        total_posts: Número total de fechas a generar.

    Returns:
        list[datetime]: Lista de objetos datetime con las fechas exactas de publicación.
    """
    dias_num = sorted({MAPA_DIAS_NUM[d] for d in dias_semana_permitidos if d in MAPA_DIAS_NUM})
    if not dias_num:
        return []

    fechas = []
    fecha_actual = fecha_inicio
    for _ in range(365):
        if len(fechas) >= total_posts:
            break
        if fecha_actual.weekday() in dias_num:
            fechas.append(datetime(fecha_actual.year, fecha_actual.month, fecha_actual.day))
        fecha_actual += timedelta(days=1)
    return fechas


def ensamblar_copy(tipo_str, tipo_operacion, colonia_estado, texto_beneficio, atributos_lista, precio, internal_id):
    """Ensambla el copy final y el primer comentario para una propiedad."""
    emoji = next((v for k, v in MAPA_EMOJI.items() if k in tipo_str.lower()), "📍")

    copy = f"{emoji} {tipo_operacion} en 📍 {colonia_estado}.\n"
    copy += f"{texto_beneficio}\n"
    if atributos_lista:
        copy += "\n".join(atributos_lista) + "\n"
    if precio:
        copy += f"💰 {precio}\n"
    copy += "📩 Agenda tu visita y contáctanos para más información.\n"
    copy += f"[{internal_id}]"

    return copy


def construir_fila_metricool(copy, fecha_dt, urls_slides, num_slides, internal_id, company, primer_comentario):
    """Construye una fila del CSV con el formato exacto de Metricool."""
    fila = {col: "" for col in COLUMNAS_METRICOOL}
    fila["Text"] = copy
    fila["Date"] = fecha_dt.strftime("%Y-%m-%d") if fecha_dt else ""
    fila["Time"] = fecha_dt.strftime("%H:%M:%S") if fecha_dt else ""
    fila["Draft"] = "FALSE"
    fila["Facebook"] = "TRUE"
    fila["Instagram"] = "TRUE"
    for k in range(num_slides):
        fila[f"Picture Url {k+1}"] = urls_slides[k] if k < len(urls_slides) else ""
    fila["Document title"] = f"Carrusel {internal_id}"
    fila["Instagram Post Type"] = "post"
    fila["Facebook Post Type"] = "post"
    fila["First Comment Text"] = primer_comentario
    fila["Brand Name"] = company
    return fila


def _clean_field(val, default=""):
    """Limpia un valor de DataFrame: retorna default si es NaN/vacío."""
    v = str(val).strip()
    return default if v.lower() == "nan" else v


# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(page_title="Automatización Metricool", layout="wide")
st.title("Automatización Metricool")
st.markdown(
    """
    Este módulo te permitirá automatizar la publicación de propiedades
    en **Metricool**, cruzando las bases de datos de inmobiliarias activas
    con las propiedades disponibles.
    """
)

# =====================================================================
# SIDEBAR
# =====================================================================
if not OPENROUTER_API_KEY:
    st.warning(
        "⚠️ No se encontró `OPENROUTER_API_KEY` en el archivo `.env`. "
        "Agrégal para generar copy con IA."
    )

st.sidebar.markdown("### 🤖 Configuración de IA")
modelo_openrouter = st.sidebar.selectbox(
    "Modelo OpenRouter",
    ("openai/gpt-oss-120b", "deepseek/deepseek-v4-flash"),
)

# =====================================================================
# PASO 1: SELECCIÓN DE BASES DE DATOS
# =====================================================================
st.markdown("---")
st.markdown("## 📂 Paso 1: Selección de Bases de Datos")

archivos_propiedades = sorted(
    DATA_DIR.glob("toppropiedades_inmobiliarias_metricool_*"),
    key=lambda p: p.stat().st_mtime,
    reverse=True,
)
archivos_inmobiliarias = sorted(
    DATA_DIR.glob("inmobiliarias_activas_en_metricool_*"),
    key=lambda p: p.stat().st_mtime,
    reverse=True,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏢 Archivo de Inmobiliarias")
    if archivos_inmobiliarias:
        archivo_inmobiliarias_seleccionado = st.selectbox(
            "Selecciona el archivo de inmobiliarias:",
            [f.name for f in archivos_inmobiliarias],
            key="select_inmobiliarias",
        )
    else:
        st.warning("No se encontraron archivos de inmobiliarias en la carpeta data/.")
        archivo_inmobiliarias_seleccionado = None

with col2:
    st.markdown("### 🏠 Archivo de Propiedades")
    if archivos_propiedades:
        archivo_propiedades_seleccionado = st.selectbox(
            "Selecciona el archivo de propiedades:",
            [f.name for f in archivos_propiedades],
            key="select_propiedades",
        )
    else:
        st.warning("No se encontraron archivos de propiedades en la carpeta data/.")
        archivo_propiedades_seleccionado = None

# --- Carga de datos ---
df_inmobiliarias = None
df_propiedades = None

if archivo_inmobiliarias_seleccionado:
    try:
        df_inmobiliarias = pd.read_csv(DATA_DIR / archivo_inmobiliarias_seleccionado)
        st.success(f"✅ Archivo de inmobiliarias cargado: **{len(df_inmobiliarias)} registros**")
    except Exception as e:
        st.error(f"Error al cargar el archivo de inmobiliarias: {e}")

if archivo_propiedades_seleccionado:
    try:
        df_propiedades = pd.read_csv(DATA_DIR / archivo_propiedades_seleccionado)
        st.success(f"✅ Archivo de propiedades cargado: **{len(df_propiedades)} registros**")
    except Exception as e:
        st.error(f"Error al cargar el archivo de propiedades: {e}")

# =====================================================================
# PASO 2: SELECCIÓN DE INMOBILIARIAS (MARCAS)
# =====================================================================
st.markdown("---")
st.markdown("## 🏷️ Paso 2: Selección de Inmobiliarias (Marcas)")

marcas_seleccionadas = []

if df_inmobiliarias is not None and "Name" in df_inmobiliarias.columns:
    marcas = sorted(df_inmobiliarias["Name"].dropna().unique().tolist())

    if "seleccion_marcas" not in st.session_state:
        st.session_state.seleccion_marcas = {m: True for m in marcas}

    col_select, col_deselect, _ = st.columns([1, 1, 4])
    with col_select:
        if st.button("✅ Seleccionar todas"):
            st.session_state.seleccion_marcas = {m: True for m in marcas}
            st.rerun()
    with col_deselect:
        if st.button("❌ Deseleccionar todas"):
            st.session_state.seleccion_marcas = {m: False for m in marcas}
            st.rerun()

    df_marcas = pd.DataFrame({
        "Seleccionar": [st.session_state.seleccion_marcas.get(m, False) for m in marcas],
        "Inmobiliaria": marcas,
    })

    edited_df = st.data_editor(
        df_marcas,
        column_config={
            "Seleccionar": st.column_config.CheckboxColumn("Seleccionar", default=True),
            "Inmobiliaria": st.column_config.TextColumn("Inmobiliaria", disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        key="editor_marcas",
    )

    if edited_df is not None:
        for _, row in edited_df.iterrows():
            st.session_state.seleccion_marcas[row["Inmobiliaria"]] = row["Seleccionar"]

    marcas_seleccionadas = [m for m, sel in st.session_state.seleccion_marcas.items() if sel]
    num_marcas = len(marcas_seleccionadas)

    if num_marcas > 0:
        st.success(f"Has seleccionado **{num_marcas}** inmobiliarias de **{len(marcas)}** disponibles.")
    else:
        st.warning("⚠️ No has seleccionado ninguna inmobiliaria.")
elif df_inmobiliarias is not None:
    st.error("El archivo de inmobiliarias no contiene la columna 'Name'. Verifica que el formato del CSV sea correcto.")
else:
    st.info("Selecciona un archivo de inmobiliarias en el Paso 1 para continuar.")

# =====================================================================
# PASO 3: CADENCIA Y SELECCIÓN ALEATORIA
# =====================================================================
st.markdown("---")
st.markdown("## 🎲 Paso 3: Cadencia y Selección")

if marcas_seleccionadas and df_propiedades is not None:
    col_fecha, col_cant = st.columns(2)
    with col_fecha:
        fecha_inicio = st.date_input(
            "Fecha de inicio de publicaciones",
            value=date.today() + timedelta(days=1),
            key="date_inicio",
        )
    with col_cant:
        cantidad_por_marca = st.slider(
            "Cantidad de propiedades a publicar por marca",
            min_value=1, max_value=20, value=3,
            key="slider_cantidad",
        )

    col_dias, col_horarios = st.columns(2)
    with col_dias:
        dias_semana = st.multiselect(
            "Días de publicación",
            list(MAPA_DIAS_NUM.keys()),
            default=["Lunes", "Miércoles", "Viernes"],
            key="multiselect_dias",
        )
    with col_horarios:
        horarios_seleccionados = st.multiselect(
            "Horarios de publicación",
            HORARIOS_DISPONIBLES,
            default=["10:00", "14:00", "18:00"],
            key="multiselect_horarios",
        )

    total_pub = len(dias_semana) * len(horarios_seleccionados) * cantidad_por_marca
    st.markdown(
        f"**Publicaciones programadas:** {len(dias_semana)} días × "
        f"{len(horarios_seleccionados)} horarios × {cantidad_por_marca} propiedades/marca "
        f"= **{total_pub} publicaciones**"
    )

    if st.button("🎲 Seleccionar Propiedades Aleatorias", type="primary", key="btn_seleccion_aleatoria"):
        historial_path = OUTPUT_DIR / "historial_publicaciones.csv"
        ids_publicados = set()
        if historial_path.exists():
            historial = pd.read_csv(historial_path)
            if "InternalId" in historial.columns:
                ids_publicados = set(historial["InternalId"].tolist())

        if "Company: Name" in df_propiedades.columns:
            propiedades_filtradas = df_propiedades[
                df_propiedades["Company: Name"].isin(marcas_seleccionadas)
                & ~df_propiedades["InternalId"].isin(ids_publicados)
            ]

            seleccionadas = []
            for marca in marcas_seleccionadas:
                propiedades_marca = propiedades_filtradas[propiedades_filtradas["Company: Name"] == marca]
                n_sample = min(cantidad_por_marca, len(propiedades_marca))
                if n_sample > 0:
                    seleccionadas.append(propiedades_marca.sample(n=n_sample, random_state=None))

            if seleccionadas:
                df_seleccionadas = pd.concat(seleccionadas, ignore_index=True)
                st.session_state["propiedades_seleccionadas"] = df_seleccionadas
                st.success(
                    f"✅ Se seleccionaron **{len(df_seleccionadas)} propiedades** de forma aleatoria. "
                    f"({len(ids_publicados)} ya publicadas fueron excluidas)"
                )
            else:
                st.warning("⚠️ No se encontraron propiedades disponibles para las marcas seleccionadas.")
                st.session_state["propiedades_seleccionadas"] = None
        else:
            st.error("El archivo de propiedades no contiene la columna 'Company: Name'.")

    if "propiedades_seleccionadas" in st.session_state and st.session_state["propiedades_seleccionadas"] is not None:
        df_sel = st.session_state["propiedades_seleccionadas"]
        st.markdown("### 📋 Propiedades Seleccionadas")
        st.dataframe(
            df_sel[["InternalId", "Company: Name", "Type", "Listing: Price: Price", "Address: Street"]].head(50),
            use_container_width=True,
            hide_index=True,
        )
else:
    if not marcas_seleccionadas:
        st.info("Selecciona al menos una inmobiliaria en el Paso 2 para continuar.")
    elif df_propiedades is None:
        st.info("Selecciona un archivo de propiedades en el Paso 1 para continuar.")

# =====================================================================
# PASO 4: DESCARGA DE FOTOS (MULTIHILO)
# =====================================================================
st.markdown("---")
st.markdown("## 📥 Paso 4: Descarga de Fotos")

if "propiedades_seleccionadas" in st.session_state and st.session_state["propiedades_seleccionadas"] is not None:
    df_descargar = st.session_state["propiedades_seleccionadas"]

    if st.button("📥 Descargar/Verificar Fotos de la Selección", type="primary", key="btn_descargar_fotos"):
        tareas = []
        for _, row in df_descargar.iterrows():
            internal_id = str(row["InternalId"]).strip()
            company_clean = re.sub(r"[^A-Za-z0-9]+", "_", str(row["Company: Name"]).strip()).strip("_")
            pictures_raw = str(row.get("Pictures", ""))

            if pd.isna(row.get("Pictures")) or pictures_raw.lower() == "nan" or not pictures_raw.strip():
                continue

            urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
            if not urls:
                continue

            property_folder = FOTOS_DIR / company_clean / internal_id
            property_folder.mkdir(parents=True, exist_ok=True)

            total_fotos = len(urls)
            for i, url in enumerate(urls):
                save_path = property_folder / f"{internal_id}-photo-{i+1:02d}-de-{total_fotos:02d}.jpg"
                tareas.append((url, save_path, internal_id))

        if not tareas:
            st.warning("No se encontraron fotos para descargar en las propiedades seleccionadas.")
        else:
            total_tareas = len(tareas)
            progress_bar = st.progress(0, text=f"Preparando {total_tareas} descargas...")
            status_empty = st.empty()

            completadas = descargadas_total = saltadas_total = 0

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {}
                for url, save_path, internal_id in tareas:
                    if save_path.exists():
                        saltadas_total += 1
                        completadas += 1
                        continue
                    futures[executor.submit(process_and_save_image, url, save_path)] = (internal_id, save_path)

            status_empty.info(f"📸 Descargando **{len(futures)} fotos** en paralelo ({total_tareas - len(futures)} ya existentes)...")

            for future in as_completed(futures):
                completadas += 1
                try:
                    if future.result():
                        descargadas_total += 1
                except Exception:
                    pass
                progress_bar.progress(completadas / total_tareas, text=f"Procesando {completadas}/{total_tareas} fotos...")

            progress_bar.progress(1.0, text="¡Completado!")
            status_empty.success(
                f"✅ Descarga finalizada: **{descargadas_total} fotos descargadas**, "
                f"**{saltadas_total} fotos ya existentes** (saltadas)."
            )
            st.session_state["fotos_descargadas"] = True

    st.info("💡 La descarga local es opcional. Si la omites, el renderizado utilizará las fotografías directamente desde la nube.")
else:
    st.info("Selecciona propiedades aleatorias en el Paso 3 para descargar sus fotos.")

# =====================================================================
# PASO 5: PREVISUALIZACIÓN (CONTROL DE CALIDAD)
# =====================================================================
st.markdown("---")
st.markdown("## 👁️ Paso 5: Previsualización (Control de Calidad)")

if "propiedades_seleccionadas" in st.session_state and st.session_state["propiedades_seleccionadas"] is not None:
    df_preview = st.session_state["propiedades_seleccionadas"]

    col_prop, col_plantilla = st.columns(2)
    with col_prop:
        seleccion_preview = st.selectbox(
            "Selecciona una propiedad para previsualizar:",
            [f"{row['InternalId']} — {row['Company: Name']}" for _, row in df_preview.iterrows()],
            key="select_preview_propiedad",
        )
    with col_plantilla:
        seleccion_plantilla = st.selectbox(
            "Selecciona la plantilla:",
            list(PLANTILLAS_DISPONIBLES.keys()),
            key="select_preview_plantilla",
        )

    if seleccion_preview and seleccion_plantilla:
        st.session_state["plantilla_seleccionada"] = seleccion_plantilla
        internal_id_preview = seleccion_preview.split(" — ")[0].strip()
        fila_preview = df_preview[df_preview["InternalId"] == internal_id_preview].iloc[0]

        if st.session_state.get("fotos_descargadas", False):
            datos_propiedad, _, _, _ = procesar_fila_a_payload_local(fila_preview)
        else:
            datos_propiedad, _, _, _ = procesar_fila_a_payload(fila_preview)

        if datos_propiedad:
            html_crudo = PLANTILLAS_DISPONIBLES[seleccion_plantilla](datos_propiedad)
            html_preview = html_crudo.replace("overflow: hidden;", "overflow: auto;").replace("overflow-hidden", "overflow-auto")

            width_total = 5400
            escala = 0.3
            html_con_escala = (
                f'<div style="width: {width_total * escala}px; height: {1350 * escala}px; overflow: hidden;">'
                f'<div style="transform: scale({escala}); transform-origin: top left; '
                f'width: {width_total}px; height: 1350px;">{html_preview}</div></div>'
            )

            st.markdown(f"**Previsualización:** {seleccion_plantilla}")
            components.html(html_con_escala, height=int(1350 * escala) + 20, scrolling=True)
        else:
            st.warning("⚠️ No se pudo generar la previsualización para esta propiedad.")
else:
    st.info("Selecciona propiedades en el Paso 3 para habilitar la previsualización.")

# =====================================================================
# PASO 6: EXPORTACIÓN FINAL
# =====================================================================
st.markdown("---")
st.markdown("## 🚀 Paso 6: Exportación Final")

st.markdown(
    "Genera los diseños, sube las imágenes a Google Drive y exporta el CSV "
    "listo para importar en Metricool."
)

if st.button("🚀 Generar Diseños, Subir a Drive y Exportar CSV", type="primary", key="btn_exportar_final"):
    # --- Validaciones previas ---
    if not OPENROUTER_API_KEY:
        st.error("⚠️ Configura la variable `OPENROUTER_API_KEY` en tu archivo `.env`.")
        st.stop()

    if "propiedades_seleccionadas" not in st.session_state or st.session_state["propiedades_seleccionadas"] is None:
        st.error("⚠️ No hay propiedades seleccionadas.")
        st.stop()

    df_exportar = st.session_state["propiedades_seleccionadas"]

    # --- 1. Conectar a Google Drive ---
    with st.status("🔌 Conectando con Google Drive...", expanded=True) as status_conexion:
        try:
            drive_service = get_drive_service()
            folder_id = get_or_create_folder(drive_service, "Carruseles_Metricool")
            status_conexion.update(label="✅ Conectado a Google Drive (carpeta: Carruseles_Metricool)", state="complete")
        except Exception as e:
            status_conexion.update(label=f"❌ Error al conectar: {e}", state="error")
            st.stop()

    hti = Html2Image(custom_flags=["--disable-gpu", "--hide-scrollbars"])

    # --- 2. Calcular fechas (INDEPENDIENTE de las marcas) ---
    fechas_dt = calcular_fechas_publicacion(fecha_inicio, dias_semana, cantidad_por_marca)

    # Convertir a strings para el CSV (con horarios rotativos)
    fechas_slots = []
    for dt in fechas_dt:
        for horario in sorted(horarios_seleccionados):
            h, m = horario.split(":")
            fechas_slots.append(dt.replace(hour=int(h), minute=int(m)))

    # Si hay menos slots que publicaciones, reciclar desde el inicio
    while len(fechas_slots) < cantidad_por_marca:
        fechas_slots.extend(fechas_slots[:cantidad_por_marca - len(fechas_slots)])

    # --- 3. Preparar iteración: fecha × marca ---
    lista_plantillas = list(PLANTILLAS_DISPONIBLES.values())
    propiedades_por_marca = {
        marca: df_exportar[df_exportar["Company: Name"] == marca]
        for marca in marcas_seleccionadas
    }

    progress_bar = st.progress(0, text="Iniciando procesamiento...")
    status_progreso = st.empty()
    filas_csv = []
    indice_global = 0
    total_propiedades = len(df_exportar)

    # --- 4. Bucle: primero por fecha, luego por marca ---
    # GARANTÍA: todas las marcas publican en las MISMAS fechas.
    for i_slot in range(cantidad_por_marca):
        fecha_dt = fechas_slots[i_slot] if i_slot < len(fechas_slots) else None

        for marca in marcas_seleccionadas:
            propiedades_marca = propiedades_por_marca[marca]

            if i_slot >= len(propiedades_marca):
                continue  # Esta marca no tiene propiedad para este slot

            row = propiedades_marca.iloc[i_slot]
            internal_id = str(row["InternalId"]).strip()
            company = str(row["Company: Name"]).strip()
            company_clean = re.sub(r"[^A-Za-z0-9]+", "_", company).strip("_")

            indice_global += 1
            status_progreso.info(f"🏭 Procesando **{indice_global}/{total_propiedades}**: {internal_id} ({company})")

            # a. Obtener payload
            if st.session_state.get("fotos_descargadas", False):
                datos_propiedad, _, _, _ = procesar_fila_a_payload_local(row)
            else:
                datos_propiedad, _, _, _ = procesar_fila_a_payload(row)
            if not datos_propiedad:
                continue

            # b. Generar copy con IA
            texto_beneficio = generar_copy_propiedad(datos_propiedad, OPENROUTER_API_KEY, modelo_openrouter)

            tipo_str = _clean_field(row.get("Type", ""))
            tipo_operacion = datos_propiedad.get("tipo_operacion", "")
            colonia_estado = datos_propiedad.get("colonia_estado", "")
            precio = datos_propiedad.get("precio", "")

            # Atributos con emojis
            attr_config = [
                (row.get("Attributes: Suites", ""), ("Habitación", "Habitaciones"), "🛏️"),
                (row.get("Attributes: Bathrooms", ""), ("Baño", "Baños"), "🛁"),
                (row.get("Attributes: Parkings", ""), ("Estacionamiento", "Estacionamientos"), "🚗"),
                (row.get("Attributes: TotalSurface", ""), "m² Totales", "📐"),
            ]
            atributos_lista = [
                f"{emoji} {formatear_atributo(v, s)}"
                for v, s, emoji in attr_config
                if formatear_atributo(v, s)
            ]

            copy_final = ensamblar_copy(tipo_str, tipo_operacion, colonia_estado, texto_beneficio, atributos_lista, precio, internal_id)

            # Primer comentario
            id_largo = _clean_field(row.get("ID", ""))
            enlace_pulppo = f"https://pulppo.com/{id_largo}" if id_largo else ""
            primer_comentario = f"Conoce todos los detalles de esta propiedad haciendo clic en este enlace: {enlace_pulppo}"

            # c. Renderizar plantilla
            funcion_plantilla = lista_plantillas[indice_global % len(lista_plantillas)]
            html_final = funcion_plantilla(datos_propiedad)
            num_slides_plantilla = MAPA_SLIDES_POR_PLANTILLA.get(funcion_plantilla, 5)
            master_width = num_slides_plantilla * 1080

            ruta_propiedad = OUTPUT_DIR / company_clean / internal_id
            ruta_propiedad.mkdir(parents=True, exist_ok=True)
            hti.output_path = str(ruta_propiedad)

            nombre_master = f"{internal_id}_master.png"
            hti.screenshot(html_str=html_final, save_as=nombre_master, size=(master_width, 1350))

            # d. Cortar master en slides y subir a Drive
            ruta_master = ruta_propiedad / nombre_master
            if ruta_master.exists():
                img_master = Image.open(ruta_master)
                urls_slides = []

                for slide_idx in range(num_slides_plantilla):
                    corte = (slide_idx * 1080, 0, (slide_idx + 1) * 1080, 1350)
                    slide_img = img_master.crop(corte)
                    ruta_slide = ruta_propiedad / f"slide_{slide_idx + 1}.png"
                    slide_img.save(ruta_slide)
                    urls_slides.append(upload_image_to_drive(drive_service, ruta_slide, folder_id))

                filas_csv.append(
                    construir_fila_metricool(copy_final, fecha_dt, urls_slides, num_slides_plantilla, internal_id, company, primer_comentario)
                )

            # e. Registrar en historial
            historial_path = OUTPUT_DIR / "historial_publicaciones.csv"
            df_hist = pd.DataFrame([{"InternalId": internal_id}])
            if historial_path.exists():
                df_hist.to_csv(historial_path, mode="a", header=False, index=False)
            else:
                df_hist.to_csv(historial_path, index=False)

            progress_bar.progress(indice_global / total_propiedades, text=f"Completado {indice_global}/{total_propiedades}")

    # --- 5. Exportar CSV final ---
    if filas_csv:
        df_csv_final = pd.DataFrame(filas_csv, columns=COLUMNAS_METRICOOL)
        csv_path = OUTPUT_DIR / "metricool_final_para_importar.csv"
        df_csv_final.to_csv(csv_path, index=False)

        total_slides = sum(
            MAPA_SLIDES_POR_PLANTILLA.get(lista_plantillas[i % len(lista_plantillas)], 5)
            for i in range(len(filas_csv))
        )

        progress_bar.progress(1.0, text="¡Proceso completado!")
        status_progreso.success(
            f"✅ **Lote completado exitosamente!**\n\n"
            f"- **{len(filas_csv)} propiedades** procesadas\n"
            f"- **{total_slides} slides** subidos a Google Drive\n"
            f"- CSV exportado a: `{csv_path}`"
        )
        st.balloons()
    else:
        st.warning("⚠️ No se generaron datos para exportar.")
