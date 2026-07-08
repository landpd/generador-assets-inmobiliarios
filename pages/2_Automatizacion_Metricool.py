import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta
from pathlib import Path
from config import DATA_DIR, OUTPUT_DIR, FOTOS_DIR, LOGOS_DIR

# Importar funciones reutilizables
from Descarga_fotos_propiedades import process_and_save_image
from google_drive_manager import get_drive_service, upload_image_to_drive, get_or_create_folder
from openai import OpenAI
from html2image import Html2Image
from PIL import Image
import plantillas_carruseles_inmobiliarias

# Diccionario de plantillas disponibles
PLANTILLAS_DISPONIBLES = {
    "Arquetipo A: Arquitectónico Minimalista": plantillas_carruseles_inmobiliarias.disenio_landscape_5fotos,
    "Arquetipo B: Elegancia Editorial": plantillas_carruseles_inmobiliarias.disenio_editorial_5fotos,
    "Arquetipo C: Bloque Corporativo": plantillas_carruseles_inmobiliarias.disenio_corporativo_5fotos,
}


# =====================================================================
# FUNCIONES AUXILIARES LOCALES
# =====================================================================
def local_image_to_base64(filepath):
    """Convierte una imagen local a base64 data URI."""
    path = Path(filepath)
    if not path.exists():
        return ""
    try:
        encoded = base64.b64encode(path.read_bytes()).decode('utf-8')
        ext = path.suffix.lower()
        mime_type = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime_type};base64,{encoded}"
    except Exception:
        return ""


def formatear_atributo(valor, sufijos):
    """Formatea un atributo numérico con su sufijo correspondiente."""
    val_str = str(valor).strip()
    if val_str.lower() in ['nan', 'none', '', '0', '0.0']:
        return ""
    if val_str.endswith('.0'):
        val_str = val_str[:-2]

    if isinstance(sufijos, tuple):
        sufijo_final = sufijos[0] if val_str == "1" else sufijos[1]
    else:
        sufijo_final = sufijos

    return f"{val_str} {sufijo_final}"


def procesar_fila_a_payload_local(row):
    """
    Convierte una fila de Pandas en el diccionario datos_propiedad.
    Lee las fotos optimizadas desde FOTOS_DIR en lugar de descargarlas de internet.
    """
    internal_id = str(row['InternalId']).strip()
    if internal_id == 'nan':
        return None, None, None, None

    company_raw = str(row.get('Company: Name', 'Inmobiliaria')).strip()
    if company_raw.lower() == 'nan':
        company_raw = "Inmobiliaria"
    company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_raw).strip('_')

    # --- Logo ---
    ruta_logo = LOGOS_DIR / f"{company_raw}_imagotipo_colab_negro.png"
    logo_b64 = local_image_to_base64(ruta_logo)

    # --- Fotos desde disco local ---
    property_folder = FOTOS_DIR / company_clean / internal_id

    def obtener_foto_base64(indice, total_fotos):
        """Lee la foto optimizada desde disco y la convierte a base64."""
        filename = f"{internal_id}-photo-{indice+1:02d}-de-{total_fotos:02d}.jpg"
        ruta_foto = property_folder / filename
        return local_image_to_base64(ruta_foto)

    # Contar cuántas fotos hay disponibles en disco
    pictures_raw = str(row.get('Pictures', ''))
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos_disponibles = len(urls)

    # --- Textos y metadatos ---
    calle_cruda = str(row.get('Address: Street', '')).strip()
    calle = "" if calle_cruda.lower() == 'nan' else calle_cruda.split(',')[0].strip()

    colonia = str(row.get('Address: Neighborhood: Name', '')).strip()
    if colonia.lower() == 'nan':
        colonia = ""
    estado = str(row.get('Address: State: Name', '')).strip()
    if estado.lower() == 'nan':
        estado = ""
    colonia_estado = f"{colonia}, {estado}".strip(", ")

    tipo = str(row.get('Type', '')).strip()
    if tipo.lower() == 'nan':
        tipo = ""
    operacion = str(row.get('Listing: Operation', '')).strip()
    if operacion.lower() == 'nan':
        operacion = ""
    if operacion.lower() == 'sale':
        operacion = 'Venta'
    elif operacion.lower() == 'rent':
        operacion = 'Renta'

    if tipo and operacion:
        tipo_en_operacion = f"{tipo} en {operacion}"
    elif tipo:
        tipo_en_operacion = tipo
    elif operacion:
        tipo_en_operacion = operacion
    else:
        tipo_en_operacion = ""

    precio_crudo = str(row.get('Listing: Price: Price', '0')).strip()
    moneda_crudo = str(row.get('Listing: Price: Currency', 'mxn')).strip().lower()
    if moneda_crudo in ['nan', '']:
        moneda_crudo = "mxn"
    precio_limpio = precio_crudo.replace(',', '').replace('$', '').replace(' ', '')
    try:
        precio_formateado = f"${float(precio_limpio):,.2f} {moneda_crudo}"
    except (ValueError, TypeError):
        precio_formateado = precio_crudo if precio_crudo.lower() != 'nan' else ""

    # --- Atributos ---
    attr_list = []
    for val, sufijo_data in [
        (row.get('Attributes: Suites', ''), ('HABITACIÓN', 'HABITACIONES')),
        (row.get('Attributes: Bathrooms', ''), ('BAÑO', 'BAÑOS')),
        (row.get('Attributes: Parkings', ''), ('ESTACIONAMIENTO', 'ESTACIONAMIENTOS')),
        (row.get('Attributes: TotalSurface', ''), 'm² TOTALES'),
    ]:
        attr = formatear_atributo(val, sufijo_data)
        if attr:
            attr_list.append(attr)

    atributos_html = "".join([f"<div>{a}</div>" for a in attr_list])

    # --- Ensamblar payload con fotos locales ---
    datos_propiedad = {
        "img1": obtener_foto_base64(0, total_fotos_disponibles),
        "img2": obtener_foto_base64(1, total_fotos_disponibles),
        "img3": obtener_foto_base64(2, total_fotos_disponibles),
        "img4": obtener_foto_base64(3, total_fotos_disponibles),
        "img5": obtener_foto_base64(4, total_fotos_disponibles),
        "img6": obtener_foto_base64(5, total_fotos_disponibles),
        "img7": obtener_foto_base64(6, total_fotos_disponibles),
        "img8": obtener_foto_base64(7, total_fotos_disponibles),
        "img9": obtener_foto_base64(8, total_fotos_disponibles),
        "logo": logo_b64,
        "tipo_operacion": tipo_en_operacion,
        "precio": precio_formateado,
        "colonia_estado": colonia_estado,
        "calle": calle,
        "atributos_html": atributos_html,
    }

    return datos_propiedad, internal_id, company_clean, company_raw


def generar_copy_propiedad(datos_propiedad, api_key, modelo_seleccionado):
    """
    Genera SOLO el texto de beneficio (1-2 líneas) usando OpenRouter.
    El ensamblaje final del copy se hace por código en el Paso 6.

    Args:
        datos_propiedad: Diccionario con los datos de la propiedad.
        api_key: API key de OpenRouter.
        modelo_seleccionado: Modelo a usar (ej. 'openai/gpt-oss-120b').

    Returns:
        str: Texto de beneficio generado por la IA (sin emojis, sin hashtags).
    """
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
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": contexto},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Una excelente oportunidad que no puedes dejar pasar por su gran ubicación y espacios."


def obtener_emoji_propiedad(tipo_str):
    """Retorna un emoji representativo según el tipo de propiedad."""
    t = tipo_str.lower()
    if 'condominio' in t:
        return '🏘️'
    elif 'casa' in t:
        return '🏠'
    elif 'departamento' in t or 'apartment' in t:
        return '🏬'
    elif 'terreno' in t or 'land' in t or 'lote' in t:
        return '🏗️'
    elif 'oficina' in t:
        return '🏢'
    elif 'local' in t:
        return '🏪'
    else:
        return '📍'


def calcular_fechas(fecha_inicio, dias_semana, horarios, total_publicaciones):
    """
    Calcula las fechas de publicación distribuyendo slots sobre días y horarios.

    Args:
        fecha_inicio: Objeto date con la fecha de inicio.
        dias_semana: Lista de strings con los días válidos
                     (ej. ['Lunes', 'Miércoles', 'Viernes']).
        horarios: Lista de strings con los horarios (ej. ['10:00', '14:00']).
        total_publicaciones: Número total de fechas a generar.

    Returns:
        list[str]: Lista de strings con formato 'DD/MM/YYYY HH:MM'.
    """
    # Mapeo de nombres de día a números (0=Lunes, 6=Domingo)
    MAPA_DIAS = {
        "Lunes": 0, "Martes": 1, "Miércoles": 2,
        "Jueves": 3, "Viernes": 4, "Sábado": 5, "Domingo": 6,
    }
    dias_num = sorted([MAPA_DIAS[d] for d in dias_semana if d in MAPA_DIAS])

    if not dias_num or not horarios:
        return []

    fechas = []
    fecha_actual = fecha_inicio
    max_dias_busqueda = 365  # Límite de seguridad

    for _ in range(max_dias_busqueda):
        if len(fechas) >= total_publicaciones:
            break

        if fecha_actual.weekday() in dias_num:
            for horario in sorted(horarios):
                if len(fechas) >= total_publicaciones:
                    break
                h, m = horario.split(":")
                dt = datetime(fecha_actual.year, fecha_actual.month, fecha_actual.day,
                              int(h), int(m))
                fechas.append(dt.strftime("%d/%m/%Y %H:%M"))

        fecha_actual += timedelta(days=1)

    return fechas

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
# CONFIGURACIÓN EN SIDEBAR
# =====================================================================
st.sidebar.markdown("### 🤖 Configuración de IA")
api_key_openrouter = st.sidebar.text_input(
    "API Key de OpenRouter", type="password"
)
modelo_openrouter = st.sidebar.selectbox(
    "Modelo OpenRouter",
    ("openai/gpt-oss-120b", "deepseek/deepseek-v4-flash"),
)

# =====================================================================
# PASO 1: SELECCIÓN DE BASES DE DATOS
# =====================================================================
st.markdown("---")
st.markdown("## 📂 Paso 1: Selección de Bases de Datos")

# Buscar archivos de propiedades (empiezan con toppropiedades_inmobiliarias_metricool_)
archivos_propiedades = sorted(
    DATA_DIR.glob("toppropiedades_inmobiliarias_metricool_*"),
    key=lambda p: p.stat().st_mtime,
    reverse=True,  # Más nuevos primero
)

# Buscar archivos de inmobiliarias (empiezan con inmobiliarias_activas_en_metricool_)
archivos_inmobiliarias = sorted(
    DATA_DIR.glob("inmobiliarias_activas_en_metricool_*"),
    key=lambda p: p.stat().st_mtime,
    reverse=True,  # Más nuevos primero
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏢 Archivo de Inmobiliarias")
    if archivos_inmobiliarias:
        nombres_inmobiliarias = [f.name for f in archivos_inmobiliarias]
        archivo_inmobiliarias_seleccionado = st.selectbox(
            "Selecciona el archivo de inmobiliarias:",
            nombres_inmobiliarias,
            key="select_inmobiliarias",
        )
    else:
        st.warning("No se encontraron archivos de inmobiliarias en la carpeta data/.")
        archivo_inmobiliarias_seleccionado = None

with col2:
    st.markdown("### 🏠 Archivo de Propiedades")
    if archivos_propiedades:
        nombres_propiedades = [f.name for f in archivos_propiedades]
        archivo_propiedades_seleccionado = st.selectbox(
            "Selecciona el archivo de propiedades:",
            nombres_propiedades,
            key="select_propiedades",
        )
    else:
        st.warning("No se encontraron archivos de propiedades en la carpeta data/.")
        archivo_propiedades_seleccionado = None

# =====================================================================
# CARGA DE DATOS
# =====================================================================
df_inmobiliarias = None
df_propiedades = None

if archivo_inmobiliarias_seleccionado:
    try:
        df_inmobiliarias = pd.read_csv(DATA_DIR / archivo_inmobiliarias_seleccionado)
        st.success(
            f"✅ Archivo de inmobiliarias cargado: **{len(df_inmobiliarias)} registros**"
        )
    except Exception as e:
        st.error(f"Error al cargar el archivo de inmobiliarias: {e}")

if archivo_propiedades_seleccionado:
    try:
        df_propiedades = pd.read_csv(DATA_DIR / archivo_propiedades_seleccionado)
        st.success(
            f"✅ Archivo de propiedades cargado: **{len(df_propiedades)} registros**"
        )
    except Exception as e:
        st.error(f"Error al cargar el archivo de propiedades: {e}")

# =====================================================================
# PASO 2: SELECCIÓN DE INMOBILIARIAS (MARCAS)
# =====================================================================
st.markdown("---")
st.markdown("## 🏷️ Paso 2: Selección de Inmobiliarias (Marcas)")

marcas_seleccionadas = []

if df_inmobiliarias is not None and "Name" in df_inmobiliarias.columns:
    # Obtener lista única de inmobiliarias
    marcas = df_inmobiliarias["Name"].dropna().unique().tolist()
    marcas.sort()

    # Inicializar session state para selección
    if "seleccion_marcas" not in st.session_state:
        st.session_state.seleccion_marcas = {marca: True for marca in marcas}

    # Botones de seleccionar/deseleccionar todas
    col_select, col_deselect, col_info = st.columns([1, 1, 4])

    with col_select:
        if st.button("✅ Seleccionar todas"):
            st.session_state.seleccion_marcas = {marca: True for marca in marcas}
            st.rerun()

    with col_deselect:
        if st.button("❌ Deseleccionar todas"):
            st.session_state.seleccion_marcas = {marca: False for marca in marcas}
            st.rerun()

    # Crear DataFrame para el data_editor
    df_marcas = pd.DataFrame(
        {
            "Seleccionar": [
                st.session_state.seleccion_marcas.get(marca, False) for marca in marcas
            ],
            "Inmobiliaria": marcas,
        }
    )

    # Editor interactivo
    edited_df = st.data_editor(
        df_marcas,
        column_config={
            "Seleccionar": st.column_config.CheckboxColumn(
                "Seleccionar",
                default=True,
            ),
            "Inmobiliaria": st.column_config.TextColumn(
                "Inmobiliaria",
                disabled=True,
            ),
        },
        use_container_width=True,
        hide_index=True,
        key="editor_marcas",
    )

    # Actualizar session state con las selecciones del editor
    if edited_df is not None:
        for _, row in edited_df.iterrows():
            st.session_state.seleccion_marcas[row["Inmobiliaria"]] = row["Seleccionar"]

    # Contar marcas seleccionadas
    marcas_seleccionadas = [
        marca for marca, seleccionada in st.session_state.seleccion_marcas.items()
        if seleccionada
    ]
    num_marcas = len(marcas_seleccionadas)

    # Mostrar resumen
    if num_marcas > 0:
        st.success(
            f"Has seleccionado **{num_marcas}** inmobiliarias de **{len(marcas)}** disponibles."
        )
    else:
        st.warning("⚠️ No has seleccionado ninguna inmobiliaria.")

else:
    if df_inmobiliarias is not None:
        st.error(
            "El archivo de inmobiliarias no contiene la columna 'Name'. "
            "Verifica que el formato del CSV sea correcto."
        )
    else:
        st.info(
            "Selecciona un archivo de inmobiliarias en el Paso 1 para continuar."
        )

# =====================================================================
# PASO 3: CADENCIA Y SELECCIÓN ALEATORIA
# =====================================================================
st.markdown("---")
st.markdown("## 🎲 Paso 3: Cadencia y Selección")

if marcas_seleccionadas and df_propiedades is not None:
    # Filtros de cadencia
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
            min_value=1,
            max_value=20,
            value=3,
            key="slider_cantidad",
        )

    col_dias, col_horarios = st.columns(2)

    with col_dias:
        dias_semana = st.multiselect(
            "Días de publicación",
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
            default=["Lunes", "Miércoles", "Viernes"],
            key="multiselect_dias",
        )

    with col_horarios:
        horarios_disponibles = [
            "08:00", "09:00", "10:00", "11:00", "12:00",
            "13:00", "14:00", "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
        ]
        horarios_seleccionados = st.multiselect(
            "Horarios de publicación",
            horarios_disponibles,
            default=["10:00", "14:00", "18:00"],
            key="multiselect_horarios",
        )

    total_pub = len(dias_semana) * len(horarios_seleccionados) * cantidad_por_marca
    st.markdown(
        f"**Publicaciones programadas:** {len(dias_semana)} días × "
        f"{len(horarios_seleccionados)} horarios × {cantidad_por_marca} propiedades/marca "
        f"= **{total_pub} publicaciones**"
    )

    # Botón de selección aleatoria
    if st.button("🎲 Seleccionar Propiedades Aleatorias", type="primary", key="btn_seleccion_aleatoria"):
        # 1. Leer historial para descartar InternalIds ya publicados (NO guardar nada aquí)
        historial_path = OUTPUT_DIR / "historial_publicaciones.csv"
        if historial_path.exists():
            historial = pd.read_csv(historial_path)
            ids_publicados = set(historial["InternalId"].tolist()) if "InternalId" in historial.columns else set()
        else:
            ids_publicados = set()

        # 2. Filtrar: solo marcas seleccionadas Y que NO estén en el historial
        if "Company: Name" in df_propiedades.columns:
            propiedades_filtradas = df_propiedades[
                (df_propiedades["Company: Name"].isin(marcas_seleccionadas)) &
                (~df_propiedades["InternalId"].isin(ids_publicados))
            ]

            # 3. Muestra aleatoria por cada marca
            seleccionadas = []
            for marca in marcas_seleccionadas:
                propiedades_marca = propiedades_filtradas[
                    propiedades_filtradas["Company: Name"] == marca
                ]
                n_sample = min(cantidad_por_marca, len(propiedades_marca))
                if n_sample > 0:
                    muestra = propiedades_marca.sample(n=n_sample, random_state=None)
                    seleccionadas.append(muestra)

            if seleccionadas:
                df_seleccionadas = pd.concat(seleccionadas, ignore_index=True)
                st.session_state['propiedades_seleccionadas'] = df_seleccionadas
                st.success(
                    f"✅ Se seleccionaron **{len(df_seleccionadas)} propiedades** de forma aleatoria. "
                    f"({len(ids_publicados)} ya publicadas fueron excluidas)"
                )
            else:
                st.warning(
                    "⚠️ No se encontraron propiedades disponibles para las marcas seleccionadas "
                    "(todas ya fueron publicadas o no hay propiedades)."
                )
                st.session_state['propiedades_seleccionadas'] = None
        else:
            st.error("El archivo de propiedades no contiene la columna 'Company: Name'.")

    # 4. Mostrar tabla de propiedades seleccionadas (si existen en session_state)
    if 'propiedades_seleccionadas' in st.session_state and st.session_state['propiedades_seleccionadas'] is not None:
        df_sel = st.session_state['propiedades_seleccionadas']
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

if 'propiedades_seleccionadas' in st.session_state and st.session_state['propiedades_seleccionadas'] is not None:
    df_descargar = st.session_state['propiedades_seleccionadas']

    if st.button("📥 Descargar/Verificar Fotos de la Selección", type="primary", key="btn_descargar_fotos"):
        # --- 1. Construir lista plana de tareas (url, save_path) ---
        tareas = []
        for _, row in df_descargar.iterrows():
            internal_id = str(row['InternalId']).strip()
            company_name = str(row['Company: Name']).strip()
            company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_name).strip('_')
            pictures_raw = str(row.get('Pictures', ''))

            if pd.isna(row.get('Pictures')) or pictures_raw.lower() == 'nan' or pictures_raw.strip() == '':
                continue

            urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
            if not urls:
                continue

            property_folder = FOTOS_DIR / company_clean / internal_id
            property_folder.mkdir(parents=True, exist_ok=True)

            total_fotos = len(urls)
            for i, url in enumerate(urls):
                filename = f"{internal_id}-photo-{i+1:02d}-de-{total_fotos:02d}.jpg"
                save_path = property_folder / filename
                tareas.append((url, save_path, internal_id))

        if not tareas:
            st.warning("No se encontraron fotos para descargar en las propiedades seleccionadas.")
        else:
            total_tareas = len(tareas)
            progress_bar = st.progress(0, text=f"Preparando {total_tareas} descargas...")
            status_empty = st.empty()

            completadas = 0
            descargadas_total = 0
            saltadas_total = 0

            # --- 2. Ejecutar descargas en paralelo ---
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {}
                for url, save_path, internal_id in tareas:
                    # Si ya existe, contar como saltada sin enviar a hilo
                    if save_path.exists():
                        saltadas_total += 1
                        completadas += 1
                        continue
                    future = executor.submit(process_and_save_image, url, save_path)
                    futures[future] = (internal_id, save_path)

                total_paralelo = len(futures)
                status_empty.info(f"📸 Descargando **{total_paralelo} fotos** en paralelo ({total_tareas - total_paralelo} ya existentes)...")

                for future in as_completed(futures):
                    internal_id, save_path = futures[future]
                    completadas += 1
                    try:
                        exito = future.result()
                        if exito:
                            descargadas_total += 1
                        else:
                            saltadas_total += 0  # Error, no contabilizar como salto
                    except Exception:
                        pass  # Error en el hilo, ya contabilizado

                    progress_bar.progress(
                        completadas / total_tareas,
                        text=f"Procesando {completadas}/{total_tareas} fotos...",
                    )

            progress_bar.progress(1.0, text="¡Completado!")
            status_empty.success(
                f"✅ Descarga finalizada: **{descargadas_total} fotos descargadas**, "
                f"**{saltadas_total} fotos ya existentes** (saltadas)."
            )
            st.session_state['fotos_descargadas'] = True
else:
    st.info("Selecciona propiedades aleatorias en el Paso 3 para descargar sus fotos.")

# =====================================================================
# PASO 5: PREVISUALIZACIÓN (CONTROL DE CALIDAD)
# =====================================================================
st.markdown("---")
st.markdown("## 👁️ Paso 5: Previsualización (Control de Calidad)")

if ('propiedades_seleccionadas' in st.session_state and
        st.session_state['propiedades_seleccionadas'] is not None and
        st.session_state.get('fotos_descargadas', False)):

    df_preview = st.session_state['propiedades_seleccionadas']

    col_prop, col_plantilla = st.columns(2)

    with col_prop:
        opciones_propiedades = [
            f"{row['InternalId']} — {row['Company: Name']}"
            for _, row in df_preview.iterrows()
        ]
        seleccion_preview = st.selectbox(
            "Selecciona una propiedad para previsualizar:",
            opciones_propiedades,
            key="select_preview_propiedad",
        )

    with col_plantilla:
        seleccion_plantilla = st.selectbox(
            "Selecciona la plantilla:",
            list(PLANTILLAS_DISPONIBLES.keys()),
            key="select_preview_plantilla",
        )

    if seleccion_preview and seleccion_plantilla:
        # Guardar la plantilla seleccionada en session_state para el Paso 6
        st.session_state['plantilla_seleccionada'] = seleccion_plantilla

        # Obtener el InternalId de la selección
        internal_id_preview = seleccion_preview.split(" — ")[0].strip()

        # Buscar la fila correspondiente
        fila_preview = df_preview[df_preview["InternalId"] == internal_id_preview].iloc[0]

        # Procesar la fila a payload usando fotos locales (sin descargar de internet)
        datos_propiedad, _, _, _ = procesar_fila_a_payload_local(fila_preview)

        if datos_propiedad:
            # Generar HTML con la plantilla seleccionada
            funcion_plantilla = PLANTILLAS_DISPONIBLES[seleccion_plantilla]
            html_preview = funcion_plantilla(datos_propiedad)

            # Escalar para previsualización
            html_escalado = f'''<div style="transform: scale(0.3); transform-origin: top left; width: 5400px; height: 1350px;">{html_preview}</div>'''

            st.markdown(f"**Previsualización:** {seleccion_plantilla}")
            components.html(html_escalado, height=450, scrolling=True)
        else:
            st.warning("⚠️ No se pudo generar la previsualización para esta propiedad.")
else:
    if 'propiedades_seleccionadas' not in st.session_state or st.session_state['propiedades_seleccionadas'] is None:
        st.info("Selecciona propiedades en el Paso 3 para habilitar la previsualización.")
    elif not st.session_state.get('fotos_descargadas', False):
        st.info("Primero descarga las fotos en el Paso 4 para habilitar la previsualización.")

# =====================================================================
# PASO 6: EXPORTACIÓN FINAL
# =====================================================================
st.markdown("---")
st.markdown("## 🚀 Paso 6: Exportación Final")

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

if st.session_state.get('fotos_descargadas', False):

    st.markdown(
        "Genera los diseños, sube las imágenes a Google Drive y exporta el CSV "
        "listo para importar en Metricool."
    )

    if st.button(
        "🚀 Generar Diseños, Subir a Drive y Exportar CSV",
        type="primary",
        key="btn_exportar_final",
    ):
        # --- Validaciones previas ---
        if not api_key_openrouter:
            st.error("⚠️ Ingresa una API Key de OpenRouter en el menú lateral.")
            st.stop()

        if 'propiedades_seleccionadas' not in st.session_state or st.session_state['propiedades_seleccionadas'] is None:
            st.error("⚠️ No hay propiedades seleccionadas.")
            st.stop()

        df_exportar = st.session_state['propiedades_seleccionadas']
        total_propiedades = len(df_exportar)

        # --- 1. Conectar a Google Drive y obtener carpeta ---
        with st.status("🔌 Conectando con Google Drive...", expanded=True) as status_conexion:
            try:
                drive_service = get_drive_service()
                folder_id = get_or_create_folder(drive_service, "Carruseles_Metricool")
                status_conexion.update(
                    label=f"✅ Conectado a Google Drive (carpeta: Carruseles_Metricool)",
                    state="complete",
                )
            except Exception as e:
                status_conexion.update(label=f"❌ Error al conectar: {e}", state="error")
                st.stop()

        # --- 2. Configurar Html2Image ---
        hti = Html2Image(custom_flags=["--disable-gpu", "--hide-scrollbars"])

        # --- 3. Calcular fechas de publicación ---
        fechas_calculadas = calcular_fechas(
            fecha_inicio, dias_semana, horarios_seleccionados, total_propiedades
        )

        # Si hay menos fechas que propiedades, reutilizar desde el inicio
        while len(fechas_calculadas) < total_propiedades:
            fechas_calculadas.extend(fechas_calculadas[:total_propiedades - len(fechas_calculadas)])

        # --- 4. Lista de plantillas para rotación dinámica ---
        lista_plantillas = list(PLANTILLAS_DISPONIBLES.values())

        # --- 5. Bucle principal de procesamiento ---
        progress_bar = st.progress(0, text="Iniciando procesamiento...")
        status_progreso = st.empty()
        filas_csv = []

        for i, (_, row) in enumerate(df_exportar.iterrows()):
            internal_id = str(row['InternalId']).strip()
            company = str(row['Company: Name']).strip()
            company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company).strip('_')
            fecha_pub_str = fechas_calculadas[i] if i < len(fechas_calculadas) else "N/A"

            # Parsear fecha y hora (DD/MM/YYYY HH:MM)
            try:
                dt_pub = datetime.strptime(fecha_pub_str, "%d/%m/%Y %H:%M")
                fecha_date = dt_pub.strftime("%Y-%m-%d")
                fecha_time = dt_pub.strftime("%H:%M:%S")
            except (ValueError, TypeError):
                fecha_date = ""
                fecha_time = ""

            status_progreso.info(
                f"🏭 Procesando **{i+1}/{total_propiedades}**: "
                f"{internal_id} ({company})"
            )

            # a. Obtener payload
            datos_propiedad, _, _, _ = procesar_fila_a_payload_local(row)
            if not datos_propiedad:
                continue

            # b. Generar texto de beneficio con IA
            texto_beneficio = generar_copy_propiedad(
                datos_propiedad, api_key_openrouter, modelo_openrouter
            )

            # --- ENSAMBLAJE ESTRUCTURADO DEL COPY FINAL ---
            # Extraer datos de la fila para armar el copy
            tipo_str = str(row.get('Type', '')).strip()
            if tipo_str.lower() == 'nan':
                tipo_str = ""
            tipo_en_operacion = datos_propiedad.get('tipo_operacion', '')
            emoji_tipo = obtener_emoji_propiedad(tipo_str)
            colonia_estado = datos_propiedad.get('colonia_estado', '')

            # Atributos con emojis
            attr_list = []
            config_atributos = [
                (row.get('Attributes: Suites', ''), ('Habitación', 'Habitaciones'), '🛏️'),
                (row.get('Attributes: Bathrooms', ''), ('Baño', 'Baños'), '🛁'),
                (row.get('Attributes: Parkings', ''), ('Estacionamiento', 'Estacionamientos'), '🚗'),
                (row.get('Attributes: TotalSurface', ''), 'm² Totales', '📐'),
            ]
            for val, sufijo_data, emoji_attr in config_atributos:
                attr_texto = formatear_atributo(val, sufijo_data)
                if attr_texto:
                    attr_list.append(f"{emoji_attr} {attr_texto}")
            atributos_finales = "\n".join(attr_list)

            precio_formateado = datos_propiedad.get('precio', '')

            # Ensamblar copy final
            copy_final = f"{emoji_tipo} {tipo_en_operacion} en 📍 {colonia_estado}.\n"
            copy_final += f"{texto_beneficio}\n"
            if atributos_finales:
                copy_final += f"{atributos_finales}\n"
            if precio_formateado:
                copy_final += f"💰 {precio_formateado}\n"
            copy_final += "📩 Agenda tu visita y contáctanos para más información.\n"
            copy_final += f"[{internal_id}]"

            # Primer comentario
            id_largo = str(row.get('ID', '')).strip()
            if id_largo.lower() == 'nan':
                id_largo = ""
            enlace_pulppo = f"https://pulppo.com/{id_largo}" if id_largo else ""
            primer_comentario = f"Conoce todos los detalles de esta propiedad haciendo clic en este enlace: {enlace_pulppo}"

            # c. Renderizar plantilla ROTADA y guardar master
            funcion_plantilla = lista_plantillas[i % len(lista_plantillas)]
            html_final = funcion_plantilla(datos_propiedad)

            ruta_propiedad = OUTPUT_DIR / company_clean / internal_id
            ruta_propiedad.mkdir(parents=True, exist_ok=True)
            hti.output_path = str(ruta_propiedad)

            nombre_master = f"{internal_id}_master.jpg"
            hti.screenshot(
                html_str=html_final,
                save_as=nombre_master,
                size=(5400, 1350),
            )

            # d. Cortar master en 5 slides y subir a Drive
            ruta_master = ruta_propiedad / nombre_master
            if ruta_master.exists():
                img_master = Image.open(ruta_master)
                urls_slides = []

                for slide_idx in range(5):
                    corte = (slide_idx * 1080, 0, (slide_idx + 1) * 1080, 1350)
                    slide_img = img_master.crop(corte)
                    nombre_slide = f"slide_{slide_idx + 1}.jpg"
                    ruta_slide = ruta_propiedad / nombre_slide
                    slide_img.save(ruta_slide, quality=95)

                    # e. Subir slide a Google Drive (dentro de la carpeta)
                    url_slide = upload_image_to_drive(drive_service, ruta_slide, folder_id)
                    urls_slides.append(url_slide)

                # f. Armar fila con el formato exacto de Metricool
                fila = {col: "" for col in COLUMNAS_METRICOOL}

                # Llenar solo las columnas relevantes
                fila["Text"] = copy_final
                fila["Date"] = fecha_date
                fila["Time"] = fecha_time
                fila["Draft"] = "FALSE"
                fila["Facebook"] = "TRUE"
                fila["Instagram"] = "TRUE"
                for j in range(5):
                    fila[f"Picture Url {j+1}"] = urls_slides[j] if j < len(urls_slides) else ""
                fila["Document title"] = f"Carrusel {internal_id}"
                fila["Instagram Post Type"] = "post"
                fila["Facebook Post Type"] = "post"
                fila["First Comment Text"] = primer_comentario
                fila["Brand Name"] = company

                filas_csv.append(fila)

            # g. Registrar en historial (append)
            historial_path = OUTPUT_DIR / "historial_publicaciones.csv"
            df_historial_nuevo = pd.DataFrame([{"InternalId": internal_id}])
            if historial_path.exists():
                df_historial_nuevo.to_csv(historial_path, mode='a', header=False, index=False)
            else:
                df_historial_nuevo.to_csv(historial_path, index=False)

            # Actualizar barra de progreso
            progress_bar.progress(
                (i + 1) / total_propiedades,
                text=f"Completado {i + 1}/{total_propiedades}",
            )

        # --- 6. Exportar CSV final con columnas exactas de Metricool ---
        if filas_csv:
            df_csv_final = pd.DataFrame(filas_csv, columns=COLUMNAS_METRICOOL)
            csv_path = OUTPUT_DIR / "metricool_final_para_importar.csv"
            df_csv_final.to_csv(csv_path, index=False)

            progress_bar.progress(1.0, text="¡Proceso completado!")
            status_progreso.success(
                f"✅ **Lote completado exitosamente!**\n\n"
                f"- **{len(filas_csv)} propiedades** procesadas\n"
                f"- **{len(filas_csv) * 5} slides** subidos a Google Drive\n"
                f"- CSV exportado a: `{csv_path}`"
            )
            st.balloons()
        else:
            st.warning("⚠️ No se generaron datos para exportar.")
