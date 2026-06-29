# ==========================================
# CELDA 2: DESCARGA DE LOGOTIPOS DE INMOBILIARIAS (DESDE GOOGLE SHEETS)
# ==========================================

import os
import re
import io
import requests
import pandas as pd
from PIL import Image
from google.colab import drive, auth
from google.auth import default
import gspread

# 1. Montar Google Drive
drive.mount('/content/drive')

# 2. Autenticar para poder leer el Google Sheet por su ID
print("Autenticando usuario para acceder a Google Sheets...")
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# 3. Definir las rutas y el ID del archivoa
SHEET_ID = "1c-Fn8oKREJc1bJpRg4JVQYNgSfTAee-m0qtrDmsvnIQ"
RUTA_LOGOS = "/content/drive/MyDrive/Nuevos proyectos/Logos Inmobiliarias"

# Crear la carpeta destino si no existe
os.makedirs(RUTA_LOGOS, exist_ok=True)

# 4. Función para descargar y guardar el logo en PNG
def download_and_save_logo(url, save_path):
    try:
        # Descargar la imagen
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # Abrir imagen con Pillow para asegurar que el formato sea procesado correctamente
        img = Image.open(io.BytesIO(response.content))

        # Guardar forzosamente como PNG (conservando transparencias originales)
        img.save(save_path, format="PNG")
        return True

    except Exception as e:
        print(f"     [!] Error procesando {url}: {e}")
        return False

# 5. Leer los datos desde Google Sheets
print(f"Conectando al archivo de Sheets con ID: {SHEET_ID}...\n")
worksheet = gc.open_by_key(SHEET_ID).sheet1 # Abre la primera pestaña
data = worksheet.get_all_values()

# Convertir los datos a un DataFrame de Pandas (la fila 0 son los encabezados)
df = pd.DataFrame(data[1:], columns=data[0])

# 6. Procesar filas y descargar ambos logos
for index, row in df.iterrows():
    # Obtener valores por nombre de columna
    raw_name = str(row.get('Nombre Inmobiliaria', '')).strip()
    url_inmo = str(row.get('logo_inmo', '')).strip()
    url_colab = str(row.get('logo_colab', '')).strip()

    # Ignorar si no hay datos de nombre o está vacío
    if not raw_name or raw_name.lower() == 'nan':
        continue

    # Limpiar el nombre para quitar caracteres no válidos en archivos
    safe_name = re.sub(r'[\\/*?:"<>|]', "", raw_name)

    # --- PROCESAR LOGO COLAB (Columna 3) ---
    if url_colab and url_colab.lower() != 'nan' and url_colab.startswith('http'):
        filename_colab = f"{safe_name}_imagotipo_colab_negro.png"
        save_path_colab = os.path.join(RUTA_LOGOS, filename_colab)

        if not os.path.exists(save_path_colab):
            print(f"Descargando logo_colab de: {raw_name}...")
            download_and_save_logo(url_colab, save_path_colab)
        else:
            print(f"    -> El logo_colab de {raw_name} ya existe. Omitiendo...")

    # --- PROCESAR LOGO INMO LIMPIO (Columna 2) ---
    if url_inmo and url_inmo.lower() != 'nan' and url_inmo.startswith('http'):
        # Se añade .png al final ya que Pillow siempre lo guardará como imagen PNG
        filename_inmo = f"{safe_name}_imagotipo_negro.png"
        save_path_inmo = os.path.join(RUTA_LOGOS, filename_inmo)

        if not os.path.exists(save_path_inmo):
            print(f"Descargando logo_inmo de: {raw_name}...")
            download_and_save_logo(url_inmo, save_path_inmo)
        else:
            print(f"    -> El logo_inmo de {raw_name} ya existe. Omitiendo...")

print("\n¡Proceso de descarga de logotipos completado!")