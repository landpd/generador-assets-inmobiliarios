import os
import json
import re
import copy

import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
from html2image import Html2Image
from PIL import Image
from dotenv import load_dotenv

from config import OUTPUT_DIR
from plantillas_educativas import (
    plantilla_geometria_limpia,
    plantilla_editorial_grunge,
    plantilla_cinematografica,
    plantilla_impacto_brutalista,
    plantilla_corporativo_listas,
)
import plantillas_educativas
from recursos_graficos import obtener_foto_pexels_b64

# ── Variables de entorno ──────────────────────────────────────────────
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_COLLECTION_ID = os.getenv("PEXELS_COLLECTION_ID")

# ── Mapeo de estilos → plantillas (Patrón Estrategia) ────────────────
MAPEO_PLANTILLAS = {
    "Arquetipo A: Editorial Grunge": plantilla_editorial_grunge,
    "Arquetipo B: Geometría Limpia": plantilla_geometria_limpia,
    "Arquetipo C: Impacto Brutalista": plantilla_impacto_brutalista,
    "Arquetipo D: Corporativo Listas": plantilla_corporativo_listas,
    "Arquetipo E: Cinematográfico": plantilla_cinematografica,
}

PALETA_DARK = {
    "fondo": "#212322",
    "texto": "#FAFAFA",
    "acento": "#F6BE00",
    "secundario": "#009A9A",
}

PALETA_LIGHT = {
    "fondo": "#FAFAFA",
    "texto": "#212322",
    "acento": "#F6BE00",
    "secundario": "#009A9A",
}


# ── Configuración de la página ───────────────────────────────────────
st.set_page_config(page_title="Carruseles Educativos", layout="wide")

st.title("Generador de Carruseles Educativos B2C")

st.markdown(
    """
    Este módulo te permitirá generar carruseles educativos para campañas B2C
    en redes sociales y plataformas de contenido, utilizando plantillas con
    **Tailwind CSS**.
    """
)

# =====================================================================
# CONFIGURACIÓN EN SIDEBAR
# =====================================================================
# API Key
if not OPENROUTER_API_KEY:
    st.warning(
        "⚠️ No se encontró la variable de entorno `OPENROUTER_API_KEY`. "
        "Agrécala al archivo `.env` del proyecto para poder generar contenido."
    )

st.sidebar.markdown("### 🤖 Configuración de IA")
modelo = st.sidebar.selectbox(
    "Modelo",
    ("deepseek/deepseek-v4-flash", "tencent/hy3-preview", "openai/gpt-oss-120b"),
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Estilo del Carrusel")
estilo = st.sidebar.selectbox(
    "Selecciona el estilo:",
    tuple(MAPEO_PLANTILLAS.keys()),
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌓 Tema de Color")
tema_color = st.sidebar.radio(
    "Tema de Color",
    ["Modo Oscuro", "Modo Claro"],
    index=0,
)

paleta = PALETA_DARK if tema_color == "Modo Oscuro" else PALETA_LIGHT

# =====================================================================
# ENTRADA DE TEXTO CRUDO DESDE LA UI PRINCIPAL
# =====================================================================
st.markdown("---")
st.markdown("### 📝 Generación de Copy con IA")
texto_crudo = st.text_area(
    "Pega la información cruda (Transcripción/Tema)",
    height=200,
    placeholder="Pega aquí el texto de una transcripción, tema o nota de la que quieras extraer slides educativos...",
)

num_slides = st.slider(
    "Longitud del Carrusel (Slides)",
    min_value=3,
    max_value=10,
    value=5,
)


# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================
def _obtener_plantilla(estilo_seleccionado):
    """Resuelve el estilo seleccionado a su función de plantilla correspondiente."""
    return MAPEO_PLANTILLAS.get(estilo_seleccionado, plantilla_geometria_limpia)


def _generar_nombre_archivo(estilo_seleccionado, tema_color_sel, etiqueta):
    """Construye el nombre base para la carpeta y archivos de salida."""
    arquetipo_str = estilo_seleccionado.split(":")[0].strip().replace(" ", "_").lower()
    tema_str = "dark" if tema_color_sel == "Modo Oscuro" else "light"
    etiqueta_limpia = re.sub(r"[^A-Za-z0-9]+", "_", str(etiqueta)).strip("_")
    return f"{arquetipo_str}_{tema_str}_{etiqueta_limpia}"


def _configurar_fotos_pexels():
    """Si hay credenciales de Pexels, inyecta la función de fotos como fuente."""
    if PEXELS_API_KEY and PEXELS_COLLECTION_ID:
        _key = PEXELS_API_KEY.strip()
        _col = PEXELS_COLLECTION_ID.strip()
        plantillas_educativas.obtener_foto_random_b64 = lambda: obtener_foto_pexels_b64(_key, _col)


# =====================================================================
# BOTÓN: GENERAR COPY Y GUARDAR EN SESSION STATE
# =====================================================================
if st.button("🪄 Generar Copy y Previsualizar"):
    if not OPENROUTER_API_KEY:
        st.error("⚠️ Configura la variable `OPENROUTER_API_KEY` en tu archivo `.env`.")
    elif not texto_crudo.strip():
        st.error("⚠️ Pega algún contenido en el área de texto.")
    else:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        system_msg = (
            "Actúa como un Copywriter experto en storytelling y redes sociales, especializado en el sector inmobiliario y de proptech. "
            "Objetivo: transformar la información cruda proporcionada en un guion de carrusel atractivo, emocional y persuasivo. "
            "ESTILO Y TONO: Persuasivo, de autoridad y empático. Conecta el valor financiero con el impacto de vida del cliente. Lenguaje directo y minimalista. "
            "ENFOQUE DE MARCA (PULPPO): Si el tema involucra procesos, comisiones o asesores inmobiliarios, DEBES posicionar al asesor como un aliado estratégico indispensable. Habla siempre de forma sumamente positiva de los brokers profesionales y de la red de Pulppo, incentivando al cliente a buscar su asesoría para evitar riesgos. NUNCA los presentes como un gasto negativo o evitable. "
            "GRAMÁTICA (ESTRICTO): Usa reglas del español. TODA oración y título DEBE iniciar con mayúscula. NO uses mayúsculas después de dos puntos (:) a menos que sea nombre propio. NO uses 'Title Case' (no capitalices la primera letra de cada palabra en los títulos). "
            "FORMATO MARKDOWN: Usa **negritas** dentro del contenido de la llave 'texto' para resaltar las palabras o frases más impactantes. "
            f"ESTRUCTURA: Genera EXACTAMENTE {num_slides} slides. "
            "1. Slide 1 (Portada): El 'titulo' DEBE ser un gancho persuasivo usando figuras retóricas (metáfora, hipérbole, pregunta) que despierte curiosidad. "
            "2. Slides intermedios: Desarrollo del contenido, 1 o 2 párrafos cortos por slide. "
            "3. Último Slide (CTA): Conclusión de valor. El llamado a la acción DEBE invitar explícitamente a 'guardar este post' y 'seguirnos' para más contenido. "
            "Para la llave 'etiqueta', NUNCA uses palabras genéricas como 'Portada', 'Slide' o 'Introducción'. Genera siempre un micro-título conceptual, llamativo y en mayúsculas (ej. 'CONSEJO FINANCIERO', 'EL MITO DE VENDER', 'ESTRATEGIA CLAVE'). "
            "FORMATO DE ENTREGA: Devuelve ESTRICTAMENTE un array JSON puro, sin formato Markdown (sin ```json), donde cada objeto tenga exactamente las llaves: etiqueta, titulo, texto, numero_slide."
        )
        try:
            with st.spinner("Generando copy con IA..."):
                response = client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": texto_crudo},
                    ],
                )
            contenido = response.choices[0].message.content

            try:
                datos_json = json.loads(contenido)
            except json.JSONDecodeError:
                st.error("El modelo no devolvió un JSON válido.")
                st.markdown("#### 📄 Respuesta cruda del modelo (para depuración):")
                st.write(contenido)
            else:
                st.session_state["json_carrusel"] = datos_json
                st.session_state["gen_id"] = st.session_state.get("gen_id", 0) + 1
                st.success("¡Copy generado exitosamente!")

        except Exception as e:
            st.error(f"❌ Error al llamar a OpenRouter: {e}")

# =====================================================================
# PREVISUALIZACIÓN EN VIVO (desde session state)
# =====================================================================
if "json_carrusel" in st.session_state:

    # ── MODO EDITOR ──────────────────────────────────────────────────
    with st.expander("✏️ Editar Textos del Carrusel", expanded=False):
        json_editado = copy.deepcopy(st.session_state["json_carrusel"])

        for i, slide in enumerate(json_editado):
            st.markdown(f"**Slide {i + 1}**")
            slide["etiqueta"] = st.text_input(
                f"Etiqueta {i + 1}",
                value=slide.get("etiqueta", ""),
                key=f"editor_e_{i}_{st.session_state.get('gen_id', 0)}",
            )
            slide["titulo"] = st.text_input(
                f"Título {i + 1}",
                value=slide.get("titulo", ""),
                key=f"editor_t_{i}_{st.session_state.get('gen_id', 0)}",
            )
            slide["texto"] = st.text_area(
                f"Texto {i + 1}",
                value=slide.get("texto", ""),
                key=f"editor_txt_{i}_{st.session_state.get('gen_id', 0)}",
            )
            st.divider()

        if st.button("🔄 Actualizar Previsualización"):
            st.session_state["json_carrusel"] = json_editado
            st.rerun()

    # ── RENDERIZADO DE PREVISUALIZACIÓN ──────────────────────────────
    st.markdown("### 👁️ Previsualización en Vivo")

    datos_array = st.session_state["json_carrusel"]

    _configurar_fotos_pexels()

    renderizar = _obtener_plantilla(estilo)
    html_crudo = renderizar(datos_array, paleta)

    width_total = 1080 * len(datos_array)
    escala = 0.3
    html_preview = html_crudo.replace("overflow: hidden;", "overflow: auto;")
    html_con_escala = (
        f'<div style="width: {width_total * escala}px; height: {1350 * escala}px; overflow: hidden;">'
        f'<div style="transform: scale({escala}); transform-origin: top left; '
        f'width: {width_total}px; height: 1350px;">{html_preview}</div></div>'
    )
    components.html(html_con_escala, height=int(1350 * escala) + 20, scrolling=True)

    # =================================================================
    # BOTÓN: RENDERIZAR Y GUARDAR PNGs
    # =================================================================
    if st.button("💾 Renderizar y Guardar PNGs", type="primary"):
        hti = Html2Image(custom_flags=["--disable-gpu", "--hide-scrollbars"])

        etiqueta_cruda = st.session_state["json_carrusel"][0].get("etiqueta", "carrusel")
        nombre_base = _generar_nombre_archivo(estilo, tema_color, etiqueta_cruda)

        ruta_salida = OUTPUT_DIR / nombre_base
        ruta_salida.mkdir(parents=True, exist_ok=True)
        hti.output_path = str(ruta_salida)

        with st.spinner("Renderizando imágenes en alta calidad..."):
            html_crudo = renderizar(datos_array, paleta)
            width_total = 1080 * len(datos_array)

            nombre_master = f"{nombre_base}_master.png"
            hti.screenshot(
                html_str=html_crudo,
                save_as=nombre_master,
                size=(width_total, 1350),
            )

            img_pano = Image.open(ruta_salida / nombre_master)
            for i in range(len(datos_array)):
                corte = (i * 1080, 0, (i + 1) * 1080, 1350)
                slide_img = img_pano.crop(corte)
                nombre_slide = f"{nombre_base}_{i + 1}.png"
                slide_img.save(ruta_salida / nombre_slide)

        st.success(f"¡Imágenes guardadas exitosamente en: {ruta_salida}")
        st.balloons()
