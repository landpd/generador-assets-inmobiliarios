# =============================================
# CELDA 01 - SELECCIÓN DE CARRUSELES A PUBLICAR
# =============================================

import os
import glob
import pandas as pd
from google.colab import drive
import random
import google.generativeai as genai
drive.mount('/content/drive')

# ==========================================
# 1. CONFIGURACIONES Y RUTAS
# ==========================================
RUTA_BASE_DATOS = "/content/drive/MyDrive/Nuevos proyectos/CSV Metabase"
RUTA_CARPETA_DISENOS = "/content/drive/MyDrive/Nuevos proyectos/Diseños_Generados"
RUTA_HISTORIAL = "/content/drive/MyDrive/Nuevos proyectos/historial_publicaciones.csv"

# Configuración de Gemini 2.5 Flash
API_KEY = 'AQ.Ab8RN6LPGQ154Hy-esrp0CIXN1XEZ943LAlA92JxWF3veAi30Q'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

CANTIDAD_A_PUBLICAR = 8

# ==========================================
# 2. ENCONTRAR EL CSV MÁS RECIENTE
# ==========================================
patron_busqueda = os.path.join(RUTA_BASE_DATOS, "propiedades_1_5_10_con_fotos_*.csv")
archivos_csv = glob.glob(patron_busqueda)

if not archivos_csv:
    raise FileNotFoundError("No se encontró ningún archivo CSV de Metabase en la ruta especificada.")

# Selecciona el archivo con la fecha de modificación más reciente
archivo_reciente = max(archivos_csv, key=os.path.getmtime)
print(f"📄 Archivo de base de datos seleccionado: {os.path.basename(archivo_reciente)}")

df_propiedades = pd.read_csv(archivo_reciente)

# ==========================================
# 3. LEER HISTORIAL Y FILTRAR DISPONIBLES
# ==========================================
if os.path.exists(RUTA_HISTORIAL):
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
    ruta_propiedad = os.path.join(RUTA_CARPETA_DISENOS, company_name, internal_id)

    if not os.path.exists(ruta_propiedad):
        print(f"❌ Carpeta no encontrada para {internal_id} (Company: {company_name})")
        continue

    # Buscar las imágenes que contengan "_carrusel_" en el nombre y sean .jpg
    patron_imagenes = os.path.join(ruta_propiedad, "*_carrusel_*.jpg")
    imagenes_encontradas = glob.glob(patron_imagenes)

    # Ordenarlas alfabéticamente (asumiendo que los números 1 al 6 las ordenan bien)
    imagenes_encontradas.sort()

    if len(imagenes_encontradas) > 0:
        print(f"✅ {internal_id} - {len(imagenes_encontradas)} imágenes de carrusel encontradas.")

        # Guardamos la fila entera y sus imágenes para usarlas en el siguiente paso
        propiedades_listas_para_publicar.append({
            "datos_ficha": row,
            "rutas_imagenes": imagenes_encontradas[:6] # Aseguramos tomar máximo 6
        })
    else:
        print(f"⚠️ {internal_id} - No se encontraron imágenes de carrusel en su carpeta.")

print(f"\n🎉 Total de propiedades validadas y listas para generar copy: {len(propiedades_listas_para_publicar)}")