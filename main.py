# ==========================================
# CELDA B: GENERADOR DE DISEÑOS MODULAR (VERSIÓN DEFINITIVA)
# ==========================================

import os
import glob
import re
import base64
import requests
import pandas as pd
import shutil
from PIL import Image
from html2image import Html2Image
from google.colab import drive

# Montar Drive (se hace una sola vez)
drive.mount('/content/drive')

# ==============================================================================
# --- 1. IMPORTAR PLANTILLAS DESDE DRIVE ---
# ==============================================================================
import sys
import importlib

RUTA_PROYECTO = "/content/drive/MyDrive/Nuevos proyectos"
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

import mis_plantillas

# OBLIGA A LEER EL ARCHIVO ACTUALIZADO CADA VEZ
importlib.reload(mis_plantillas)

# ==============================================================================
# --- 2. CONFIGURACIÓN DEL GENERADOR ---
# ==============================================================================
# --- Control de guardado ---
SOBREESCRIBIR_EXISTENTES = False

# --- Diseños a generar (Interruptores True/False) ---
PLANTILLAS_A_GENERAR = {
    "Landscape_5Fotos": {
        "activo": True,
        "funcion": mis_plantillas.disenio_landscape_5fotos,
        "width": 1920,
        "height": 1080,
        "sufijo_archivo": "landscape_5fotos"
    },
    "Post_3Fotos": {
        "activo": True,
        "funcion": mis_plantillas.disenio_vertical_3fotos,
        "width": 1080,
        "height": 1350,
        "sufijo_archivo": "post_3fotos"
    },
    "Story_Figma": {
        "activo": True,
        "funcion": mis_plantillas.disenio_story_figma,
        "width": 1080,
        "height": 1920,
        "sufijo_archivo": "story"
    },
    "Carrusel_Panoramico": {
        "activo": True,
        "funcion": mis_plantillas.disenio_carrusel_6fotos,
        "width": 6480,
        "height": 1350,
        "sufijo_archivo": "carrusel",
        "cortar_carrusel": True, # <--- Activa la guillotina de Python
        "partes": 6 # <--- En cuántos slides de Instagram se parte
    },
    "Story_Baja_Precio": {
        "activo": True,
        "funcion": mis_plantillas.disenio_oferta_baja_precio,
        "width": 1080,
        "height": 1920,
        "sufijo_archivo": "baja_precio"
    }

}

# ==============================================================================
# --- 3. CONFIGURACIÓN DEL ENTORNO Y DATOS ---
# ==============================================================================
RUTA_CSV = "/content/drive/MyDrive/Nuevos proyectos/CSV Metabase"
RUTA_SALIDA = "/content/drive/MyDrive/Nuevos proyectos/Diseños_Generados"
RUTA_LOGOS = "/content/drive/MyDrive/Nuevos proyectos/Logos Inmobiliarias"

hti = Html2Image(
    browser_executable='/usr/bin/google-chrome',
    custom_flags=['--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--disable-dev-shm-usage']
)
hti.output_path = '/content'

csv_files = glob.glob(os.path.join(RUTA_CSV, "propiedades_1_5_10_con_fotos_*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {RUTA_CSV}")

latest_csv = sorted(csv_files)[-1]
print(f"📄 Procesando base de datos: {os.path.basename(latest_csv)}")
df = pd.read_csv(latest_csv)

# --- Funciones de ayuda ---
def formatear_atributo(valor, sufijos):
    val_str = str(valor).strip()
    # Descartar nulos o ceros
    if val_str.lower() in ['nan', 'none', '', '0', '0.0']: return ""
    # Quitar el ".0" si viene como flotante
    if val_str.endswith('.0'): val_str = val_str[:-2]

    # Lógica de Singular vs Plural
    if isinstance(sufijos, tuple):
        # Si el valor es exactamente "1", toma la primera palabra, si no, la segunda
        sufijo_final = sufijos[0] if val_str == "1" else sufijos[1]
    else:
        # Si no es una tupla (ej. m² TOTALES), lo deja tal cual
        sufijo_final = sufijos

    return f"{val_str} {sufijo_final}"

def url_to_base64(url):
    if not url: return ""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        encoded = base64.b64encode(resp.content).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded}"
    except:
        return ""

def local_image_to_base64(filepath):
    if not os.path.exists(filepath):
        print(f"     ⚠️ Logo no encontrado: {os.path.basename(filepath)}")
        return ""
    try:
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')

        # Detectar la extensión para usar el formato correcto
        ext = os.path.splitext(filepath)[1].lower()
        mime_type = "image/png" if ext == ".png" else "image/jpeg"

        return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        print(f"     ⚠️ Error al leer el logo: {e}")
        return ""

# ==============================================================================
# --- 4. BUCLE PRINCIPAL DE PROCESAMIENTO Y RENDERIZADO ---
# ==============================================================================
print("\n🚀 Iniciando generación de imágenes modulares...\n")
imagenes_generadas = 0

for index, row in df.iterrows():
    internal_id = str(row['InternalId']).strip()
    if internal_id == 'nan': continue

    print(f"\nPropiedad: {internal_id}...")

    # --- LIMPIEZA DE DATOS (COMPAÑÍA) ---
    company_raw = str(row.get('Company: Name', 'Inmobiliaria')).strip()
    if company_raw.lower() == 'nan': company_raw = "Inmobiliaria"

    company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_raw).strip('_')
    company_folder = re.sub(r'[\\/*?:"<>|]', "", company_raw).strip()

    # --- CARGA DEL LOGO DE LA INMOBILIARIA (.png) ---
    nombre_logo = f"{company_raw}_imagotipo_colab_negro.png"
    ruta_logo = os.path.join(RUTA_LOGOS, nombre_logo)
    logo_b64 = local_image_to_base64(ruta_logo)

    # --- FOTOS ---
    pictures_raw = str(row['Pictures'])
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)
    if not urls: continue

    def obtener_foto(indice):
        return urls[indice] if len(urls) > indice else urls[0]

    img1_b64 = url_to_base64(obtener_foto(0))
    img2_b64 = url_to_base64(obtener_foto(1))
    img3_b64 = url_to_base64(obtener_foto(2))
    img4_b64 = url_to_base64(obtener_foto(3))
    img5_b64 = url_to_base64(obtener_foto(4))
    img6_b64 = url_to_base64(obtener_foto(5))
    img7_b64 = url_to_base64(obtener_foto(6))
    img8_b64 = url_to_base64(obtener_foto(7))
    img9_b64 = url_to_base64(obtener_foto(8))


    # --- TEXTOS ---
    calle_cruda = str(row.get('Address: Street', '')).strip()
    if calle_cruda.lower() == 'nan':
        calle = ""
    else:
        calle = calle_cruda.split(',')[0].strip()

    colonia = str(row.get('Address: Neighborhood: Name', '')).strip()
    if colonia.lower() == 'nan': colonia = ""
    estado = str(row.get('Address: State: Name', '')).strip()
    if estado.lower() == 'nan': estado = ""
    colonia_estado = f"{colonia}, {estado}".strip(", ")

    # --- LÓGICA: TIPO Y OPERACIÓN ---
    tipo = str(row.get('Type', '')).strip()
    if tipo.lower() == 'nan': tipo = ""
    operacion = str(row.get('Listing: Operation', '')).strip()
    if operacion.lower() == 'nan': operacion = ""

    # Capitalización forzada
    if operacion.lower() == 'sale': operacion = 'Venta'
    elif operacion.lower() == 'rent': operacion = 'Renta'

    # Unir datos (Ej. "Casa en condominio en Venta")
    if tipo and operacion:
        tipo_en_operacion = f"{tipo} en {operacion}"
    elif tipo:
        tipo_en_operacion = tipo
    elif operacion:
        tipo_en_operacion = operacion
    else:
        tipo_en_operacion = ""

    # --- LÓGICA: PRECIO ---
    precio_crudo = str(row.get('Listing: Price: Price', '0')).strip()
    moneda_crudo = str(row.get('Listing: Price: Currency', 'mxn')).strip().lower()
    if moneda_crudo == 'nan' or moneda_crudo == '': moneda_crudo = "mxn"
    precio_limpio = precio_crudo.replace(',', '').replace('$', '').replace(' ', '')

    try:
        precio_formateado = f"${float(precio_limpio):,.2f} {moneda_crudo}"
    except:
        precio_formateado = precio_crudo if precio_crudo.lower() != 'nan' else ""

    # --- LÓGICA: ATRIBUTOS PLURALIZADOS ---
    attr_list = []
    # Usamos tuplas ("Singular", "Plural") para alimentar la nueva lógica de atributos
    for val, sufijo_data in [
        (row.get('Attributes: Suites', ''), ('HABITACIÓN', 'HABITACIONES')),
        (row.get('Attributes: Bathrooms', ''), ('BAÑO', 'BAÑOS')),
        (row.get('Attributes: Parkings', ''), ('ESTACIONAMIENTO', 'ESTACIONAMIENTOS')),
        (row.get('Attributes: TotalSurface', ''), 'm² TOTALES') # Al ser string directo, no pluraliza.
    ]:
        attr = formatear_atributo(val, sufijo_data)
        if attr: attr_list.append(attr)

    atributos_html = "".join([f"<div>{a}</div>" for a in attr_list])

    # --- EMPAQUETADO DE DATOS ---
    datos_propiedad = {
        "img1": img1_b64,
        "img2": img2_b64,
        "img3": img3_b64,
        "img4": img4_b64,
        "img5": img5_b64,
        "img6": img6_b64,
        "img7": img7_b64,
        "img8": img8_b64,
        "img9": img9_b64,
        "logo": logo_b64,
        "tipo_operacion": tipo_en_operacion,
        "precio": precio_formateado,
        "colonia_estado": colonia_estado,
        "calle": calle,
        "atributos_html": atributos_html
    }

    # --- CREAR ESTRUCTURA DE CARPETAS ---
    ruta_directorio = os.path.join(RUTA_SALIDA, company_folder, internal_id)
    os.makedirs(ruta_directorio, exist_ok=True)

    # --- RENDERIZADO DINÁMICO DE PLANTILLAS ---
    for nombre_disenio, config in PLANTILLAS_A_GENERAR.items():

        # VALIDACIÓN 1: ¿El diseño está activo en la configuración?
        if not config.get("activo", True):
            continue  # Salta al siguiente diseño silenciosamente

        print(f"  -> Verificando {nombre_disenio}...")
        nombre_archivo = f"{internal_id}_{company_clean}_{config['sufijo_archivo']}.jpg"
        ruta_guardado = os.path.join(ruta_directorio, nombre_archivo)
        ruta_local = os.path.join('/content', nombre_archivo)

        # VALIDACIÓN 2: Omitir si ya existe y NO queremos sobreescribir
        if not SOBREESCRIBIR_EXISTENTES and os.path.exists(ruta_guardado):
            print(f"     ✅ El diseño {nombre_archivo} ya existe. Omitiendo...")
            continue

        print(f"  -> 🎨 Diseñando {nombre_disenio}...")

        html_final = config["funcion"](datos_propiedad)

        hti.screenshot(
            html_str=html_final,
            save_as=nombre_archivo,
            size=(config["width"], config["height"])
        )

        # --- SISTEMA DE RECORTE PANORÁMICO (LA MAGIA DEL CARRUSEL) ---
        if config.get("cortar_carrusel"):
            print(f"     ✂️ Cortando panorámica en {config['partes']} diapositivas...")

            # Abrir la imagen gigante que acaba de crear Html2Image
            img_pano = Image.open(ruta_local)
            ancho_slide = config["width"] // config["partes"] # 6480 / 6 = 1080px
            alto_slide = config["height"]

            for i in range(config["partes"]):
                # Definir coordenadas de corte (Left, Top, Right, Bottom)
                corte = (i * ancho_slide, 0, (i + 1) * ancho_slide, alto_slide)
                slide = img_pano.crop(corte)

                # Guardar el pedazo con su sufijo _1, _2, _3...
                nombre_slide = f"{internal_id}_{company_clean}_{config['sufijo_archivo']}_{i+1}.jpg"
                slide.save(os.path.join(ruta_directorio, nombre_slide), quality=95)

            # Opcional: También guardamos la panorámica original completa por si la necesitas
            shutil.move(ruta_local, ruta_guardado)
        else:
            # Flujo normal para plantillas de 1 sola imagen
            shutil.move(ruta_local, ruta_guardado)

        imagenes_generadas += 1

print(f"\n✅ ¡Proceso terminado! Se generaron {imagenes_generadas} diseños en total.")
print(f"📂 Revisa la carpeta raíz: {RUTA_SALIDA}")