import streamlit as st
import streamlit.components.v1 as components
import json
import re
import html
from pathlib import Path
from openai import OpenAI
from html2image import Html2Image
from PIL import Image
from config import OUTPUT_DIR
from plantillas_educativas import (
    plantilla_panoramica_educativa,
    plantilla_pano_cinematografica,
    plantilla_pano_geometrica,
    plantilla_individual_editorial,
    plantilla_indiv_collage,
    plantilla_indiv_tecnica,
)

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
st.sidebar.markdown("### 🤖 Configuración de IA")
api_key = st.sidebar.text_input("API Key de OpenRouter", type="password")
modelo = st.sidebar.selectbox(
    "Modelo",
    ("deepseek/deepseek-v4-flash", "tencent/hy3-preview", "openai/gpt-oss-120b"),
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Estilo del Carrusel")
estilo = st.sidebar.selectbox(
    "Selecciona el estilo:",
    (
        "Panorámico: Básico (Oscuro)",
        "Panorámico: Cinematográfico (Textura Polvo)",
        "Panorámico: Geométrico / Imagen de Stock",
        "Individual: Editorial Asimétrico",
        "Individual: Collage (Marco Polaroid)",
        "Individual: Ficha Técnica (Papel Oscuro)",
    ),
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌓 Tema de Color")
tema_color = st.sidebar.radio(
    "Tema de Color",
    ["Modo Oscuro", "Modo Claro"],
    index=0,
)

# Mapear modo a paleta de design tokens
if tema_color == "Modo Oscuro":
    paleta = {
        "fondo": "#212322",
        "texto": "#FAFAFA",
        "acento": "#F6BE00",
        "secundario": "#009A9A",
    }  # Pulppo Dark
else:
    paleta = {
        "fondo": "#FAFAFA",
        "texto": "#212322",
        "acento": "#F6BE00",
        "secundario": "#C11A00",
    }  # Pulppo Light

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
# BOTÓN: GENERAR COPY Y GUARDAR EN SESSION STATE
# =====================================================================
if st.button("🪄 Generar Copy y Previsualizar"):
    if not api_key:
        st.error("⚠️ Ingresa una API Key de OpenRouter en el menú lateral.")
    elif not texto_crudo.strip():
        st.error("⚠️ Pega algún contenido en el área de texto.")
    else:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        system_msg = (
            "Actúa como un Copywriter experto en storytelling y redes sociales, especializado en el sector inmobiliario y de proptech. "
            "Objetivo: transformar la información cruda proporcionada en un guion de carrusel atractivo, emocional y persuasivo. "
            "ESTILO Y TONO: Persuasivo, de autoridad y empático. Conecta el valor financiero con el impacto de vida del cliente. Lenguaje directo y minimalista. "
            "GRAMÁTICA (ESTRICTO): Usa reglas del español. NO uses mayúsculas después de dos puntos (:) a menos que sea nombre propio. NO uses 'Title Case' (no capitalices la primera letra de cada palabra en los títulos). "
            "FORMATO MARKDOWN: Usa **negritas** dentro del contenido de la llave 'texto' para resaltar las palabras o frases más impactantes. "
            f"ESTRUCTURA: Genera EXACTAMENTE {num_slides} slides. "
            "1. Slide 1 (Portada): El 'titulo' DEBE ser un gancho persuasivo usando figuras retóricas (metáfora, hipérbole, pregunta) que despierte curiosidad. "
            "2. Slides intermedios: Desarrollo del contenido, 1 o 2 párrafos cortos por slide. "
            "3. Último Slide (CTA): Conclusión de valor. El llamado a la acción DEBE invitar explícitamente a 'guardar este post' y 'seguirnos' para más contenido. "
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
                # Guardar en session state para persistencia y renderizado posterior
                st.session_state["json_carrusel"] = datos_json
                st.success("¡Copy generado exitosamente!")

        except Exception as e:
            st.error(f"❌ Error al llamar a OpenRouter: {e}")

# =====================================================================
# PREVISUALIZACIÓN EN VIVO (desde session state)
# =====================================================================
if "json_carrusel" in st.session_state:

    # =================================================================
    # MODO EDITOR: modificar textos del carrusel antes de renderizar
    # =================================================================
    with st.expander("✏️ Editar Textos del Carrusel", expanded=False):
        import copy

        json_editado = copy.deepcopy(st.session_state["json_carrusel"])

        for i, slide in enumerate(json_editado):
            st.markdown(f"**Slide {i + 1}**")
            slide["titulo"] = st.text_input(
                f"Título {i + 1}",
                value=slide.get("titulo", ""),
                key=f"editor_t_{i}",
            )
            slide["texto"] = st.text_area(
                f"Texto {i + 1}",
                value=slide.get("texto", ""),
                key=f"editor_txt_{i}",
            )
            st.divider()

        if st.button("🔄 Actualizar Previsualización"):
            st.session_state["json_carrusel"] = json_editado
            st.rerun()

    st.markdown("### 👁️ Previsualización en Vivo")

    datos_array = st.session_state['json_carrusel']

    # Rutear a la función correcta según el estilo (todas son panorámicas)
    if "Básico" in estilo:
        html_crudo = plantilla_panoramica_educativa(datos_array, paleta)
    elif "Cinematográfico" in estilo:
        html_crudo = plantilla_pano_cinematografica(datos_array, paleta)
    elif "Geométrico" in estilo:
        html_crudo = plantilla_pano_geometrica(datos_array, paleta)
    elif "Editorial" in estilo:
        html_crudo = plantilla_individual_editorial(datos_array, paleta)
    elif "Collage" in estilo:
        html_crudo = plantilla_indiv_collage(datos_array, paleta)
    else:
        html_crudo = plantilla_indiv_tecnica(datos_array, paleta)

    width_total = 1080 * len(datos_array)
    escala = 0.3
    # HACK: Reemplazar overflow:hidden para que el iframe permita scroll
    html_preview = html_crudo.replace('overflow: hidden;', 'overflow: auto;')
    # Envolver en contenedor restrictivo para scroll horizontal
    html_con_escala = f'''<div style="width: {width_total * escala}px; height: {1350 * escala}px; overflow: hidden;"><div style="transform: scale({escala}); transform-origin: top left; width: {width_total}px; height: 1350px;">{html_preview}</div></div>'''
    components.html(html_con_escala, height=int(1350 * escala) + 20, scrolling=True)

    # =================================================================
    # BOTÓN: RENDERIZAR Y GUARDAR JPEGs
    # =================================================================
    if st.button("💾 Renderizar y Guardar JPEGs", type="primary"):
        hti = Html2Image(custom_flags=["--disable-gpu", "--hide-scrollbars"])

        # Crear carpeta de salida basada en el título del primer slide
        titulo_limpio = re.sub(
            r"[^A-Za-z0-9]+", "_", st.session_state["json_carrusel"][0]["titulo"]
        )
        ruta_salida = OUTPUT_DIR / f"Carrusel_{titulo_limpio}"
        ruta_salida.mkdir(parents=True, exist_ok=True)
        hti.output_path = str(ruta_salida)

        with st.spinner("Renderizando imágenes..."):
            # Rutear a la función correcta (todas devuelven HTML panorámico)
            if "Básico" in estilo:
                html_crudo = plantilla_panoramica_educativa(datos_array, paleta)
            elif "Cinematográfico" in estilo:
                html_crudo = plantilla_pano_cinematografica(datos_array, paleta)
            elif "Geométrico" in estilo:
                html_crudo = plantilla_pano_geometrica(datos_array, paleta)
            elif "Editorial" in estilo:
                html_crudo = plantilla_individual_editorial(datos_array, paleta)
            elif "Collage" in estilo:
                html_crudo = plantilla_indiv_collage(datos_array, paleta)
            else:
                html_crudo = plantilla_indiv_tecnica(datos_array, paleta)

            # Renderizar master panorámico
            width_total = 1080 * len(datos_array)
            hti.screenshot(
                html_str=html_crudo,
                save_as="pano_master.jpg",
                size=(width_total, 1350),
            )

            # Cortar el master en slides individuales
            img_pano = Image.open(ruta_salida / "pano_master.jpg")
            for i in range(len(datos_array)):
                corte = (i * 1080, 0, (i + 1) * 1080, 1350)
                slide_img = img_pano.crop(corte)
                slide_img.save(
                    ruta_salida / f"slide_{i+1}.jpg",
                    quality=95,
                )

        st.success(f"¡Imágenes guardadas exitosamente en: {ruta_salida}")
        st.balloons()