import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path

from config import DATA_DIR, OUTPUT_DIR
from main import procesar_fila_a_payload, ejecutar_pipeline, PLANTILLAS_A_GENERAR

st.set_page_config(page_title="Generador de Assets", layout="wide", page_icon="⚙️")

st.title("⚙️ Generador de Assets Inmobiliarios")
st.markdown("Panel de control para previsualización y renderizado masivo.")

# --- SIDEBAR: SELECCIÓN DE DATOS ---
st.sidebar.header("📁 Origen de Datos")
archivos_csv = sorted(DATA_DIR.glob("propiedades_*.csv"), reverse=True)

if not archivos_csv:
    st.error(f"No se encontraron archivos CSV en la carpeta {DATA_DIR}")
    st.stop()

csv_seleccionado = st.sidebar.selectbox(
    "Selecciona el archivo CSV a procesar:",
    archivos_csv,
    format_func=lambda x: x.name
)

# --- CARGA DE DATOS ---
df = pd.read_csv(csv_seleccionado)
df_filtrado = df.dropna(subset=['InternalId'])

st.subheader(f"📊 Vista Previa de Datos ({len(df_filtrado)} propiedades)")
st.dataframe(df_filtrado[['InternalId', 'Company: Name', 'Listing: Operation', 'Type', 'Listing: Price: Price']].head())

# --- SECCIÓN DE PREVISUALIZACIÓN ---
st.markdown("---")
st.header("👁️ Previsualizador de Plantillas")

col1, col2 = st.columns([1, 2])

with col1:
    fila_id = st.selectbox(
        "Selecciona una propiedad (InternalId):",
        df_filtrado['InternalId'].astype(str).tolist()
    )

    plantilla_elegida = st.selectbox(
        "Selecciona la plantilla a previsualizar:",
        list(PLANTILLAS_A_GENERAR.keys())
    )

# Lógica de preview
fila_datos = df_filtrado[df_filtrado['InternalId'].astype(str) == fila_id].iloc[0]

with st.spinner('Cargando imágenes (Base64)...'):
    # Usamos la función refactorizada de main.py
    payload, internal_id, comp_clean, comp_folder = procesar_fila_a_payload(fila_datos)

if payload:
    config_plantilla = PLANTILLAS_A_GENERAR[plantilla_elegida]
    html_crudo = config_plantilla["funcion"](payload)

    with col2:
        st.markdown(f"**Vista previa: {plantilla_elegida}** ({config_plantilla['width']}x{config_plantilla['height']}px)")
        # Escalar el renderizado en la UI (zoom CSS)
        escala = 0.4 if config_plantilla['width'] > 2000 else 0.6
        html_con_escala = f"<div style='transform: scale({escala}); transform-origin: top left;'>{html_crudo}</div>"

        components.html(
            html_con_escala,
            width=int(config_plantilla['width'] * escala),
            height=int(config_plantilla['height'] * escala),
            scrolling=True
        )
else:
    st.warning("No se pudo procesar la información de esta propiedad.")

# --- SECCIÓN DE ACCIÓN (RENDERIZADO LOTE) ---
st.markdown("---")
st.header("🚀 Procesamiento por Lotes")
st.info(f"Se procesarán {len(df_filtrado)} propiedades usando html2image. El resultado irá a la carpeta de Salida.")

if st.button("Generar Todo el Lote", type="primary"):
    with st.spinner("Ejecutando html2image en segundo plano... Por favor espera."):
        total = ejecutar_pipeline(csv_seleccionado)
    st.success(f"¡Proceso completado! Se generaron {total} imágenes en la carpeta {OUTPUT_DIR}")