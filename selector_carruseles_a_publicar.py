# =============================================
# SELECCIÓN DE CARRUSELES A PUBLICAR (VERSIÓN LOCAL)
# =============================================

import pandas as pd
import random
import google.generativeai as genai

from config import DATA_DIR, OUTPUT_DIR

# ==========================================
# 1. CONFIGURACIONES Y RUTAS
# ==========================================
RUTA_HISTORIAL = OUTPUT_DIR / "historial_publicaciones.csv"

# Configuración de Gemini 2.5 Flash
API_KEY = 'AQ.Ab8RN6LPGQ154Hy-esrp0CIXN1XEZ943LAlA92JxWF3veAi30Q'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

CANTIDAD_A_PUBLICAR = 8

# ==========================================
# 2. ENCONTRAR EL CSV MÁS RECIENTE
# ==========================================
archivos_csv = sorted(DATA_DIR.glob("propiedades_1_5_10_con_fotos_*.csv"))

if not archivos_csv:
    raise FileNotFoundError("No se encontró ningún archivo CSV de Metabase en DATA_DIR.")

# Selecciona el archivo con la fecha de modificación más reciente
archivo_reciente = max(archivos_csv, key=lambda p: p.stat().st_mtime)
print(f"📄 Archivo de base de datos seleccionado: {archivo_reciente.name}")

df_propiedades = pd.read_csv(archivo_reciente)

# ==========================================
# 3. LEER HISTORIAL Y FILTRAR DISPONIBLES
# ==========================================
if RUTA_HISTORIAL.exists():
    df_historial = pd.read_csv(RUTA_HISTORIAL)
    publicados = df_historial['InternalId'].astype(str).tolist()
else:
    publicados = []

# Filtrar propiedades que no estén en el historial
df_propiedades['InternalId'] = df_propiedades['InternalId'].astype(str)
df_disponibles = df_propiedades[~df_propiedades['InternalId'].isin(publicados)]

print(f"📊 Propiedades totales: {len(df_propiedades)} | Disponibles sin publicar: {len(df_disponibles)}")

if len(df_disponibles) < CANTIDAD_A_PUBLICAR:
    print(f"⚠️ Advertencia: Solo hay {len(df_disponibles)} propiedades disponibles. Se seleccionarán todas.")
    CANTIDAD_A_PUBLICAR = len(df_disponibles)

# ==========================================
# 4. SELECCIONAR PROPIEDADES Y BUSCAR IMÁGENES
# ==========================================
# Tomamos una muestra aleatoria
propiedades_seleccionadas = df_disponibles.sample(n=CANTIDAD_A_PUBLICAR)
propiedades_listas_para_publicar = []

print("\n🔍 Buscando diseños para las propiedades seleccionadas...")

for index, row in propiedades_seleccionadas.iterrows():
    company_name = str(row['Company: Name'])
    internal_id = str(row['InternalId'])

    # Construir la ruta de la carpeta de diseños para esta propiedad
    ruta_propiedad = OUTPUT_DIR / company_name / internal_id

    if not ruta_propiedad.exists():
        print(f"❌ Carpeta no encontrada para {internal_id} (Company: {company_name})")
        continue

    # Buscar las imágenes que contengan "_carrusel_" en el nombre y sean .jpg
    imagenes_encontradas = sorted(ruta_propiedad.glob("*_carrusel_*.jpg"))

    if len(imagenes_encontradas) > 0:
        print(f"✅ {internal_id} - {len(imagenes_encontradas)} imágenes de carrusel encontradas.")

        # Guardamos la fila entera y sus imágenes para usarlas en el siguiente paso
        propiedades_listas_para_publicar.append({
            "datos_ficha": row,
            "rutas_imagenes": imagenes_encontradas[:6]
        })
    else:
        print(f"⚠️ {internal_id} - No se encontraron imágenes de carrusel en su carpeta.")

print(f"\n🎉 Total de propiedades validadas y listas para generar copy: {len(propiedades_listas_para_publicar)}")
