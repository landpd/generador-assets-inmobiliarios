import streamlit as st
import pandas as pd
from pathlib import Path
from config import DATA_DIR, OUTPUT_DIR

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
api_key_metricool = st.sidebar.text_input(
    "API Key de Metricool", type="password"
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

        # Mostrar propiedades cruzadas si también se cargó el archivo de propiedades
        if df_propiedades is not None and "Company: Name" in df_propiedades.columns:
            propiedades_filtradas = df_propiedades[
                df_propiedades["Company: Name"].isin(marcas_seleccionadas)
            ]
            st.info(
                f"📊 Se encontraron **{len(propiedades_filtradas)} propiedades** "
                f"para las {num_marcas} inmobiliarias seleccionadas."
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
