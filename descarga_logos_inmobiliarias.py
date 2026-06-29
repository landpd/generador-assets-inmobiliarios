# ==========================================
# DESCARGA DE LOGOTIPOS DE INMOBILIARIAS (VERSIÓN LOCAL)
# ==========================================

import re
import io
import requests
import pandas as pd
from PIL import Image

from config import DATA_DIR, LOGOS_DIR

# --- 1. Crear la carpeta destino si no existe ---
LOGOS_DIR.mkdir(parents=True, exist_ok=True)

# --- 2. Función para descargar y guardar el logo en PNG ---
def download_and_save_logo(url, save_path):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        img = Image.open(io.BytesIO(response.content))
        img.save(save_path, format="PNG")
        return True

    except Exception as e:
        print(f"     [!] Error procesando {url}: {e}")
        return False


# --- 3. Leer los datos desde el CSV en DATA_DIR ---
csv_files = sorted(DATA_DIR.glob("logos_inmobiliarias*.csv"))
if not csv_files:
    raise FileNotFoundError(
        f"No se encontró ningún archivo CSV de logos en: {DATA_DIR}\n"
        f"Exporta tu Google Sheet como CSV y colócalo en esa carpeta "
        f"(ej. logos_inmobiliarias.csv)"
    )

latest_csv = csv_files[-1]
print(f"Archivo CSV de logos detectado: {latest_csv.name}\n")
df = pd.read_csv(latest_csv)

# --- 4. Procesar filas y descargar ambos logos ---
for index, row in df.iterrows():
    raw_name = str(row.get('Nombre Inmobiliaria', '')).strip()
    url_inmo = str(row.get('logo_inmo', '')).strip()
    url_colab = str(row.get('logo_colab', '')).strip()

    # Ignorar si no hay nombre o está vacío
    if not raw_name or raw_name.lower() == 'nan':
        continue

    # Limpiar el nombre para quitar caracteres no válidos en archivos
    safe_name = re.sub(r'[\\/*?:"<>|]', "", raw_name)

    # --- PROCESAR LOGO COLAB ---
    if url_colab and url_colab.lower() != 'nan' and url_colab.startswith('http'):
        filename_colab = f"{safe_name}_imagotipo_colab_negro.png"
        save_path_colab = LOGOS_DIR / filename_colab

        if not save_path_colab.exists():
            print(f"Descargando logo_colab de: {raw_name}...")
            download_and_save_logo(url_colab, save_path_colab)
        else:
            print(f"    -> El logo_colab de {raw_name} ya existe. Omitiendo...")

    # --- PROCESAR LOGO INMO LIMPIO ---
    if url_inmo and url_inmo.lower() != 'nan' and url_inmo.startswith('http'):
        filename_inmo = f"{safe_name}_imagotipo_negro.png"
        save_path_inmo = LOGOS_DIR / filename_inmo

        if not save_path_inmo.exists():
            print(f"Descargando logo_inmo de: {raw_name}...")
            download_and_save_logo(url_inmo, save_path_inmo)
        else:
            print(f"    -> El logo_inmo de {raw_name} ya existe. Omitiendo...")

print("\n¡Proceso de descarga de logotipos completado!")
