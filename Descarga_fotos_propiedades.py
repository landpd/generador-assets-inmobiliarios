# ==========================================
# CELDA 1: DESCARGA Y PROCESAMIENTO DE FOTOS
# ==========================================

import os
import glob
import re
import io
import requests
import pandas as pd
from PIL import Image
from google.colab import drive

# 1. Montar Google Drive
drive.mount('/content/drive')

# 2. Definir las rutas (Ajusta mayúsculas/minúsculas si es necesario)
RUTA_CSV = "/content/drive/MyDrive/Nuevos proyectos/CSV Metabase"
RUTA_FOTOS = "/content/drive/MyDrive/Nuevos proyectos/Fotografías Propiedades 1-5-10"

# 3. Función para procesar y guardar la imagen
def process_and_save_image(url, save_path):
    try:
        # Descargar la imagen
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # Abrir imagen con Pillow
        img = Image.open(io.BytesIO(response.content))

        # Convertir a RGB (elimina transparencias si es PNG y evita errores al guardar como JPG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Redimensionar si el lado más corto es mayor a 2000 pixeles
        w, h = img.size
        shortest_side = min(w, h)

        if shortest_side > 2000:
            ratio = 2000 / shortest_side
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Comprimir hasta que pese menos de 500 KB
        quality = 95
        while quality >= 10:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            size_kb = len(buffer.getvalue()) / 1024

            if size_kb <= 500:
                with open(save_path, "wb") as f:
                    f.write(buffer.getvalue())
                return True
            quality -= 5

        # Si aún bajando la calidad a 10 no se logra (raro), se guarda con calidad 10
        with open(save_path, "wb") as f:
            f.write(buffer.getvalue())
        return True

    except Exception as e:
        print(f"     [!] Error procesando {url}: {e}")
        return False

# 4. Encontrar el archivo CSV más reciente en la RUTA_CSV
csv_files = glob.glob(os.path.join(RUTA_CSV, "propiedades_1_5_10_con_fotos_*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {RUTA_CSV}")

latest_csv = sorted(csv_files)[-1]
print(f"Archivo CSV detectado: {os.path.basename(latest_csv)}\n")

# 5. Leer CSV y procesar filas
df = pd.read_csv(latest_csv)

for index, row in df.iterrows():
    internal_id = str(row['InternalId']).strip()
    company_name = str(row['Company: Name']).strip()
    pictures_raw = str(row['Pictures'])

    # Ignorar si no hay datos de fotos o empresa
    if pd.isna(row['Pictures']) or pictures_raw.lower() == 'nan':
        continue

    # Extraer URLs usando Regex
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos = len(urls)

    if total_fotos == 0:
        continue

    print(f"Procesando {internal_id} ({company_name}) - {total_fotos} fotos encontradas...")

    # Crear carpeta de la propiedad en la RUTA_FOTOS: Company / InternalId
    property_folder = os.path.join(RUTA_FOTOS, company_name, internal_id)
    os.makedirs(property_folder, exist_ok=True)

    # Procesar cada foto
    for i, url in enumerate(urls):
        # Generar el nombre de archivo (ej. ABC-123-photo-01-de-05.jpg)
        filename = f"{internal_id}-photo-{i+1:02d}-de-{total_fotos:02d}.jpg"
        save_path = os.path.join(property_folder, filename)

        # Saltar si la foto ya existe (para reanudar sin duplicar trabajo)
        if not os.path.exists(save_path):
            process_and_save_image(url, save_path)

print("\n¡Proceso de descarga y optimización completado!")