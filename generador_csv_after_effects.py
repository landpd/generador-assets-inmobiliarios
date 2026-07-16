# ==========================================
# GENERADOR DE CSV PARA AFTER EFFECTS (VERSIÓN LOCAL)
# ==========================================

import re
import pandas as pd

from config import DATA_DIR, OUTPUT_DIR
from utils import formatear_atributo

# --- 1. Buscar el CSV de Pulppo más reciente en DATA_DIR ---
csv_files = sorted(DATA_DIR.glob("propiedades_1_5_10_con_fotos_*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {DATA_DIR}")

latest_csv = csv_files[-1]
print(f"📄 Procesando base de datos: {latest_csv.name}\n")

df = pd.read_csv(latest_csv)


def formatear_metros(valor):
    return formatear_atributo(valor, "m² TOTALES")


# --- 3. Preparar la lista de datos ---
datos_ae = []

for index, row in df.iterrows():
    internal_id = str(row['InternalId']).strip()
    if internal_id == 'nan':
        continue

    # --- NOMBRE DEL VIDEO (Composición en AE) ---
    company_raw = str(row.get('Company: Name', 'Inmobiliaria')).strip()
    if company_raw.lower() == 'nan':
        company_raw = "Inmobiliaria"
    company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_raw).strip('_')
    nombre_comp = f"{internal_id}_{company_clean}_(4-5)_Post"

    # --- CALLE ---
    calle_cruda = str(row.get('Address: Street', '')).strip()
    calle = calle_cruda if calle_cruda.lower() != 'nan' else ""

    # --- COLONIA, CIUDAD ---
    colonia = str(row.get('Address: Neighborhood: Name', '')).strip()
    if colonia.lower() == 'nan':
        colonia = ""

    ciudad = str(row.get('Address: City: Name', '')).strip()
    if ciudad.lower() == 'nan':
        ciudad = ""

    colonia_estado = f"{colonia}, {ciudad}".strip(", ")
    if colonia_estado.startswith(", "):
        colonia_estado = colonia_estado[2:]
    if colonia_estado.endswith(","):
        colonia_estado = colonia_estado[:-1]

    # --- OPERACIÓN CON CORCHETES ---
    tipo = str(row.get('Type', '')).strip()
    if tipo.lower() == 'nan':
        tipo = ""

    operacion = str(row.get('Listing: Operation', '')).strip()
    if operacion.lower() == 'nan':
        operacion = ""
    if operacion.lower() == 'sale':
        operacion = 'Venta'
    elif operacion.lower() == 'rent':
        operacion = 'Renta'

    if tipo and operacion:
        tipo_en_operacion = f"[ {tipo} en {operacion} ]"
    elif tipo:
        tipo_en_operacion = f"[ {tipo} ]"
    elif operacion:
        tipo_en_operacion = f"[ {operacion} ]"
    else:
        tipo_en_operacion = ""

    # --- PRECIO ---
    precio_crudo = str(row.get('Listing: Price: Price', '0')).strip()
    moneda_crudo = str(row.get('Listing: Price: Currency', 'mxn')).strip().lower()
    if moneda_crudo == 'nan' or moneda_crudo == '':
        moneda_crudo = "mxn"
    precio_limpio = precio_crudo.replace(',', '').replace('$', '').replace(' ', '')
    try:
        precio_formateado = f"${float(precio_limpio):,.2f} {moneda_crudo}"
    except:
        precio_formateado = precio_crudo if precio_crudo.lower() != 'nan' else ""

    # --- ATRIBUTOS FORMATEADOS ---
    habitaciones = formatear_atributo(row.get('Attributes: Suites', ''), ("HABITACIÓN", "HABITACIONES"))
    banos = formatear_atributo(row.get('Attributes: Bathrooms', ''), ("BAÑO", "BAÑOS"))
    estacionamientos = formatear_atributo(row.get('Attributes: Parkings', ''), ("ESTACIONAMIENTO", "ESTACIONAMIENTOS"))
    metros = formatear_atributo(row.get('Attributes: TotalSurface', ''), "m² TOTALES")

    # --- RECONSTRUIR NOMBRES DE ARCHIVOS MULTIMEDIA ---
    pictures_raw = str(row['Pictures'])
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos = len(urls)

    media_files = {}
    for i in range(10):
        num_media = i + 1
        key = f"Media_{num_media:02d}"

        if i < total_fotos:
            filename = f"{internal_id}-photo-{num_media:02d}-de-{total_fotos:02d}.jpg"
            media_files[key] = filename
        else:
            media_files[key] = ""

    # --- ENSAMBLAR LA FILA ---
    fila = {
        "Name": nombre_comp,
        "Calle": calle,
        "Colonia, Estado": colonia_estado,
        "inmueble en operacion": tipo_en_operacion,
        "Precio": precio_formateado,
        "habitaciones": habitaciones,
        "baños": banos,
        "estacionamientos": estacionamientos,
        "metros totales": metros
    }

    fila.update(media_files)
    datos_ae.append(fila)


# --- 4. Generar el CSV final ---
df_ae = pd.DataFrame(datos_ae)

ruta_salida = OUTPUT_DIR / "CSV_After_Effects.csv"
ruta_salida.parent.mkdir(parents=True, exist_ok=True)
df_ae.to_csv(ruta_salida.as_posix(), index=False, encoding='utf-8-sig')

print(f"✅ ¡CSV para After Effects generado con éxito!")
print(f"📂 Archivo guardado en: {ruta_salida}")

print(df_ae[['Name', 'Calle', 'Colonia, Estado', 'inmueble en operacion', 'habitaciones', 'baños']].head())
