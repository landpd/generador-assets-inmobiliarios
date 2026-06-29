# ==========================================
# DESCARGA Y PROCESAMIENTO DE FOTOS (VERSIÓN LOCAL)
# ==========================================

import re
import io
import requests
import pandas as pd
from PIL import Image

from config import DATA_DIR, FOTOS_DIR

# --- 1. Función para procesar y guardar la imagen ---
def process_and_save_image(url, save_path):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        img = Image.open(io.BytesIO(response.content))

        # Convertir a RGB si tiene transparencias
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Redimensionar si el lado más corto es mayor a 2000 píxeles
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
                save_path.write_bytes(buffer.getvalue())
                return True
            quality -= 5

        # Si aun con calidad 10 no se logra, se guarda así
        save_path.write_bytes(buffer.getvalue())
        return True

    except Exception as e:
        print(f"     [!] Error procesando {url}: {e}")
        return False


# --- 2. Encontrar el archivo CSV más reciente en DATA_DIR ---
csv_files = sorted(DATA_DIR.glob("propiedades_1_5_10_con_fotos_*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {DATA_DIR}")

latest_csv = csv_files[-1]
print(f"Archivo CSV detectado: {latest_csv.name}\n")

# --- 3. Leer CSV y procesar filas ---
df = pd.read_csv(latest_csv)

for index, row in df.iterrows():
    internal_id = str(row['InternalId']).strip()
    company_name = str(row['Company: Name']).strip()
    pictures_raw = str(row['Pictures'])

    # Ignorar si no hay datos de fotos
    if pd.isna(row['Pictures']) or pictures_raw.lower() == 'nan':
        continue

    # Extraer URLs con regex
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos = len(urls)

    if total_fotos == 0:
        continue

    print(f"Procesando {internal_id} ({company_name}) - {total_fotos} fotos encontradas...")

    # Crear carpeta: FOTOS_DIR / Company / InternalId
    property_folder = FOTOS_DIR / company_name / internal_id
    property_folder.mkdir(parents=True, exist_ok=True)

    # Procesar cada foto
    for i, url in enumerate(urls):
        filename = f"{internal_id}-photo-{i+1:02d}-de-{total_fotos:02d}.jpg"
        save_path = property_folder / filename

        if not save_path.exists():
            process_and_save_image(url, save_path)

print("\n¡Proceso de descarga y optimización completado!")
