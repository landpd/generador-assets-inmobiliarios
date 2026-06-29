# ==========================================
# CELDA C: GENERADOR DE CSV PARA AFTER EFFECTS
# ==========================================

import os
import glob
import re
import pandas as pd
from google.colab import drive

# 1. Montar Google Drive
drive.mount('/content/drive')

# 2. Definir rutas
RUTA_CSV = "/content/drive/MyDrive/Nuevos proyectos/CSV Metabase"
RUTA_GUARDADO = "/content/drive/MyDrive/Nuevos proyectos/CSV_After_Effects.csv"

# 3. Buscar el CSV de Pulppo más reciente
csv_files = glob.glob(os.path.join(RUTA_CSV, "propiedades_1_5_10_con_fotos_*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {RUTA_CSV}")

latest_csv = sorted(csv_files)[-1]
print(f"📄 Procesando base de datos: {os.path.basename(latest_csv)}\n")

df = pd.read_csv(latest_csv)

# --- Funciones de ayuda para formatear plurales y vacíos ---
def formatear_plural(valor, singular, plural):
    val_str = str(valor).strip()
    # Si está vacío o es 0, devolvemos texto vacío (Para que AE oculte los guiones)
    if val_str.lower() in ['nan', 'none', '', '0', '0.0']:
        return ""
    try:
        v_float = float(val_str)
        if v_float == 0:
            return ""
        # Si es un número entero (ej. 3.0), le quitamos el decimal
        if v_float.is_integer():
            v_int = int(v_float)
            return f"{v_int} {singular}" if v_int == 1 else f"{v_int} {plural}"
        else:
            return f"{v_float} {singular}" if v_float == 1 else f"{v_float} {plural}"
    except:
        return ""

def formatear_metros(valor):
    val_str = str(valor).strip()
    if val_str.lower() in ['nan', 'none', '', '0', '0.0']:
        return ""
    try:
        v_float = float(val_str)
        if v_float == 0:
            return ""
        if v_float.is_integer():
            return f"{int(v_float)} m² TOTALES"
        else:
            return f"{v_float} m² TOTALES"
    except:
        return ""

# 4. Preparar la lista de datos
datos_ae = []

for index, row in df.iterrows():
    internal_id = str(row['InternalId']).strip()
    if internal_id == 'nan': continue

    # --- NOMBRE DEL VIDEO (Composición en AE) ---
    company_raw = str(row.get('Company: Name', 'Inmobiliaria')).strip()
    if company_raw.lower() == 'nan': company_raw = "Inmobiliaria"
    company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_raw).strip('_')
    nombre_comp = f"{internal_id}_{company_clean}_(4-5)_Post"

    # --- CALLE Y COLONIA/CIUDAD ---
    # Calle
    calle_cruda = str(row.get('Address: Street', '')).strip()
    calle = calle_cruda if calle_cruda.lower() != 'nan' else ""

    # Colonia, Ciudad (CORREGIDO)
    colonia = str(row.get('Address: Neighborhood: Name', '')).strip()
    if colonia.lower() == 'nan': colonia = ""

    ciudad = str(row.get('Address: City: Name', '')).strip()
    if ciudad.lower() == 'nan': ciudad = ""

    # Unimos con coma, el strip evita que quede ", Ciudad" o "Colonia," si falta uno
    colonia_estado = f"{colonia}, {ciudad}".strip(", ")
    # En caso de que haya quedado una coma con espacio en los extremos
    if colonia_estado.startswith(", "): colonia_estado = colonia_estado[2:]
    if colonia_estado.endswith(","): colonia_estado = colonia_estado[:-1]

    # --- OPERACIÓN CON CORCHETES ---
    tipo = str(row.get('Type', '')).strip()
    if tipo.lower() == 'nan': tipo = ""

    operacion = str(row.get('Listing: Operation', '')).strip()
    if operacion.lower() == 'nan': operacion = ""
    if operacion.lower() == 'sale': operacion = 'Venta'
    elif operacion.lower() == 'rent': operacion = 'Renta'

    if tipo and operacion:
        tipo_en_operacion = f"[ {tipo} en {operacion} ]"
    elif tipo:
        tipo_en_operacion = f"[ {tipo} ]"
    elif operacion:
        tipo_en_operacion = f"[ {operacion} ]"
    else:
        tipo_en_operacion = ""

    # --- PRECIO (Mantenido por si decides agregarlo al video después) ---
    precio_crudo = str(row.get('Listing: Price: Price', '0')).strip()
    moneda_crudo = str(row.get('Listing: Price: Currency', 'mxn')).strip().lower()
    if moneda_crudo == 'nan' or moneda_crudo == '': moneda_crudo = "mxn"
    precio_limpio = precio_crudo.replace(',', '').replace('$', '').replace(' ', '')
    try:
        precio_formateado = f"${float(precio_limpio):,.2f} {moneda_crudo}"
    except:
        precio_formateado = precio_crudo if precio_crudo.lower() != 'nan' else ""

    # --- ATRIBUTOS FORMATEADOS ---
    # Automáticamente se encargará de singular/plural o devolver "" si es 0
    habitaciones = formatear_plural(row.get('Attributes: Suites', ''), "HABITACIÓN", "HABITACIONES")
    banos = formatear_plural(row.get('Attributes: Bathrooms', ''), "BAÑO", "BAÑOS")
    estacionamientos = formatear_plural(row.get('Attributes: Parkings', ''), "ESTACIONAMIENTO", "ESTACIONAMIENTOS")
    metros = formatear_metros(row.get('Attributes: TotalSurface', ''))

    # --- RECONSTRUIR NOMBRES DE ARCHIVOS MULTIMEDIA ---
    pictures_raw = str(row['Pictures'])
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    total_fotos = len(urls)

    media_files = {}
    for i in range(10): # Rango para Media_01 a Media_10
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

# 5. Generar el CSV final
df_ae = pd.DataFrame(datos_ae)

# Codificación utf-8-sig crucial para AE y los acentos
df_ae.to_csv(RUTA_GUARDADO, index=False, encoding='utf-8-sig')

print(f"✅ ¡CSV para After Effects generado con éxito!")
print(f"📂 Archivo guardado en: {RUTA_GUARDADO}")

display(df_ae[['Name', 'Calle', 'Colonia, Estado', 'inmueble en operacion', 'habitaciones', 'baños']].head())