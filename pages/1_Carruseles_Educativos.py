import streamlit as st
import streamlit.components.v1 as components
import json
import re
from pathlib import Path
from openai import OpenAI
from html2image import Html2Image
from PIL import Image
from config import OUTPUT_DIR
from plantillas_educativas import (
    plantilla_panoramica_educativa,
    plantilla_pano_cinematografica,
    plantilla_pano_halftone,
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
        "Panorámico: Pop/Promocional (Halftone)",
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
            "Actúa como un Copywriter experto en Real Estate Inmobiliario. "
            "Genera un array JSON puro sin formato Markdown (sin ```json ni ```). "
            "Cada elemento del array debe tener exactamente estas llaves: "
            "etiqueta, titulo, texto, numero_slide. "
            f"Genera EXACTAMENTE {num_slides} slides. "
            "El Slide 1 DEBE ser un título gancho (Portada). "
            "Los slides intermedios son el desarrollo del contenido. "
            "El ÚLTIMO slide DEBE ser una Conclusión y Call to Action (CTA). "
            "Devuelve ESTRICTAMENTE solo el JSON array, nada más."
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
                st.session_state["estilo_elegido"] = estilo
                st.success("¡Copy generado exitosamente!")

        except Exception as e:
            st.error(f"❌ Error al llamar a OpenRouter: {e}")

# =====================================================================
# PREVISUALIZACIÓN EN VIVO (desde session state)
# =====================================================================
if "json_carrusel" in st.session_state:
    datos_json = st.session_state["json_carrusel"]
    estilo_actual = st.session_state.get("estilo_elegido", estilo)

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

    if "Panorámico" in estilo_actual:
        # Regenerar HTML panorámico
        if "Básico" in estilo_actual:
            html_crudo = plantilla_panoramica_educativa(datos_json, paleta)
        elif "Cinematográfico" in estilo_actual:
            html_crudo = plantilla_pano_cinematografica(datos_json, paleta)
        else:
            html_crudo = plantilla_pano_halftone(datos_json, paleta)

        width_total = 1080 * len(st.session_state['json_carrusel'])
        escala = 0.3

        # HACK: Reemplazar el overflow:hidden temporalmente para que el iframe permita scroll
        html_preview = html_crudo.replace('overflow: hidden;', 'overflow: auto;')

        # Envolver en un contenedor restrictivo para que el scroll horizontal se adapte perfectamente al tamaño escalado
        html_con_escala = f'''
        <div style="width: {width_total * escala}px; height: {1350 * escala}px; overflow: hidden;">
            <div style="transform: scale({escala}); transform-origin: top left; width: {width_total}px; height: 1350px;">
                {html_preview}
            </div>
        </div>
        '''

        components.html(html_con_escala, height=int(1350 * escala) + 20, scrolling=True)

    elif "Individual" in estilo_actual:
        total_slides = len(datos_json)
        cols = st.columns(total_slides)
        for i, slide_data in enumerate(datos_json):
            with cols[i]:
                if "Editorial" in estilo_actual:
                    html_crudo = plantilla_individual_editorial(
                        slide_data, i, total_slides, paleta
                    )
                elif "Collage" in estilo_actual:
                    html_crudo = plantilla_indiv_collage(
                        slide_data, i, total_slides, paleta
                    )
                else:
                    html_crudo = plantilla_indiv_tecnica(
                        slide_data, i, total_slides, paleta
                    )

                escala = 0.3
                html_con_escala = (
                    f"<div style='transform: scale({escala}); "
                    f"transform-origin: top left; "
                    f"width: 1080px; height: 1350px;'>{html_crudo}</div>"
                )
                components.html(
                    html_con_escala,
                    width=350,
                    height=int(1350 * escala) + 10,
                    scrolling=False,
                )

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
            if "Panorámico" in estilo_actual:
                # Regenerar HTML panorámico completo
                if "Básico" in estilo_actual:
                    html_crudo = plantilla_panoramica_educativa(datos_json, paleta)
                elif "Cinematográfico" in estilo_actual:
                    html_crudo = plantilla_pano_cinematografica(datos_json, paleta)
                else:
                    html_crudo = plantilla_pano_halftone(datos_json, paleta)
                width_total = 1080 * len(datos_json)
                hti.screenshot(
                    html_str=html_crudo,
                    save_as="pano_master.jpg",
                    size=(width_total, 1350),
                )

                # Cortar el master en slides individuales
                img_pano = Image.open(ruta_salida / "pano_master.jpg")
                for i in range(len(datos_json)):
                    corte = (i * 1080, 0, (i + 1) * 1080, 1350)
                    slide_img = img_pano.crop(corte)
                    slide_img.save(
                        ruta_salida / f"slide_{i+1}.jpg",
                        quality=95,
                    )

            else:
                # Individual: renderizar cada slide por separado
                total_slides = len(datos_json)
                for i, slide_data in enumerate(datos_json):
                    if "Editorial" in estilo_actual:
                        html_crudo = plantilla_individual_editorial(
                            slide_data, i, total_slides, paleta
                        )
                    elif "Collage" in estilo_actual:
                        html_crudo = plantilla_indiv_collage(
                            slide_data, i, total_slides, paleta
                        )
                    else:
                        html_crudo = plantilla_indiv_tecnica(
                            slide_data, i, total_slides, paleta
                        )

                    hti.screenshot(
                        html_str=html_crudo,
                        save_as=f"slide_{i+1}.jpg",
                        size=(1080, 1350),
                    )

        st.success(f"¡Imágenes guardadas exitosamente en: {ruta_salida}")
        st.balloons()