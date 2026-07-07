# ==========================================
# DESCARGA Y PROCESAMIENTO DE FOTOS (VERSIÓN MODULAR)
# ==========================================

import re
import io
import requests
import pandas as pd
from PIL import Image

from config import DATA_DIR, FOTOS_DIR


# --- 1. Función para procesar y guardar la imagen ---
def process_and_save_image(url, save_path):
    """Descarga una imagen desde una URL, la optimiza y la guarda en save_path."""
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


# --- 2. Función principal reutilizable ---
def descargar_fotos_propiedad(row):
    """
    Descarga y optimiza las fotos de una propiedad (fila de Pandas).

    Crea la carpeta en FOTOS_DIR / company_clean / internal_id
    y descarga cada foto. Si ya existen, las salta.

    Args:
        row: Fila de Pandas con las columnas del CSV de propiedades.

    Returns:
        tuple: (internal_id, company_clean, fotos_descargadas, fotos_saltadas)
    """
    internal_id = str(row['InternalId']).strip()
    company_name = str(row['Company: Name']).strip()
    pictures_raw = str(row.get('Pictures', ''))

    # Crear company_clean (sin caracteres especiales)
    company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_name).strip('_')

    # Ignorar si no hay datos de fotos
    if pd.isna(row.get('Pictures')) or pictures_raw.lower() == 'nan' or pictures_raw.strip() == '':
        return internal_id, company_clean, 0, 0

    # Extraer URLs con regex
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos = len(urls)

    if total_fotos == 0:
        return internal_id, company_clean, 0, 0

    # Crear carpeta: FOTOS_DIR / Company / InternalId
    property_folder = FOTOS_DIR / company_clean / internal_id
    property_folder.mkdir(parents=True, exist_ok=True)

    fotos_descargadas = 0
    fotos_saltadas = 0

    # Procesar cada foto
    for i, url in enumerate(urls):
        filename = f"{internal_id}-photo-{i+1:02d}-de-{total_fotos:02d}.jpg"
        save_path = property_folder / filename

        if save_path.exists():
            fotos_saltadas += 1
        else:
            if process_and_save_image(url, save_path):
                fotos_descargadas += 1

    return internal_id, company_clean, fotos_descargadas, fotos_saltadas


# --- 3. Ejecución directa (solo al correr python Descarga_fotos_propiedades.py) ---
if __name__ == "__main__":
    csv_files = sorted(DATA_DIR.glob("propiedades_1_5_10_con_fotos_*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {DATA_DIR}")

    latest_csv = csv_files[-1]
    print(f"Archivo CSV detectado: {latest_csv.name}\n")

    df = pd.read_csv(latest_csv)

    for index, row in df.iterrows():
        internal_id, company_clean, descargadas, saltadas = descargar_fotos_propiedad(row)
        if descargadas + saltadas > 0:
            print(f"Procesando {internal_id} ({company_clean}) - {descargadas} descargadas, {saltadas} saltadas")

    print("\n¡Proceso de descarga y optimización completado!")
