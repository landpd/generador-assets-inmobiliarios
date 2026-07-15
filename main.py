# ==========================================
# GENERADOR DE DISEÑOS MODULAR (VERSIÓN LOCAL)
# ==========================================

import re
import base64
import importlib
import requests
import pandas as pd
from PIL import Image
from html2image import Html2Image
from pathlib import Path

from config import DATA_DIR, OUTPUT_DIR, LOGOS_DIR
from recursos_graficos import buscar_imagen_pexels, url_a_base64

import mis_plantillas

# OBLIGA A LEER EL ARCHIVO ACTUALIZADO CADA VEZ
importlib.reload(mis_plantillas)

# ==============================================================================
# --- 1. CONFIGURACIÓN DEL GENERADOR ---
# ==============================================================================
SOBREESCRIBIR_EXISTENTES = False

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
        "cortar_carrusel": True,
        "partes": 6
    },
    "Story_Baja_Precio": {
        "activo": True,
        "funcion": mis_plantillas.disenio_oferta_baja_precio,
        "width": 1080,
        "height": 1920,
        "sufijo_archivo": "baja_precio"
    }
}

hti = Html2Image(
    custom_flags=['--disable-gpu', '--hide-scrollbars']
)

# Obtener texturas de alta calidad desde Pexels (una sola vez)
print("🎨 Obteniendo texturas de alta calidad desde Pexels...")
url_tex_clara = buscar_imagen_pexels("white marble texture clean", "landscape")
url_tex_oscura = buscar_imagen_pexels("dark luxury modern texture", "landscape")
textura_clara_b64 = url_a_base64(url_tex_clara) if url_tex_clara else ""
textura_oscura_b64 = url_a_base64(url_tex_oscura) if url_tex_oscura else ""

# ==============================================================================
# --- 2. FUNCIONES DE AYUDA ---
# ==============================================================================
def formatear_atributo(valor, sufijos):
    val_str = str(valor).strip()
    if val_str.lower() in ['nan', 'none', '', '0', '0.0']: return ""
    if val_str.endswith('.0'): val_str = val_str[:-2]

    if isinstance(sufijos, tuple):
        sufijo_final = sufijos[0] if val_str == "1" else sufijos[1]
    else:
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
    path = Path(filepath)
    if not path.exists():
        print(f"     ⚠️ Logo no encontrado: {path.name}")
        return ""
    try:
        encoded = base64.b64encode(path.read_bytes()).decode('utf-8')
        ext = path.suffix.lower()
        mime_type = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        print(f"     ⚠️ Error al leer el logo: {e}")
        return ""

# ==============================================================================
# --- 3. EXTRACCIÓN DE DATOS (Encapsulada para la UI) ---
# ==============================================================================
def procesar_fila_a_payload(row, textura_clara_b64="", textura_oscura_b64=""):
    """Convierte una fila de Pandas en el diccionario datos_propiedad y metadatos."""
    internal_id = str(row['InternalId']).strip()
    if internal_id == 'nan': return None, None, None, None

    company_raw = str(row.get('Company: Name', 'Inmobiliaria')).strip()
    if company_raw.lower() == 'nan': company_raw = "Inmobiliaria"
    company_clean = re.sub(r'[^A-Za-z0-9]+', '_', company_raw).strip('_')
    company_folder = re.sub(r'[\\/*?:"<>|]', "", company_raw).strip()

    ruta_logo = LOGOS_DIR / f"{company_raw}_imagotipo_colab_negro.png"
    logo_b64 = local_image_to_base64(ruta_logo)

    pictures_raw = str(row['Pictures'])
    urls = re.findall(r'\[:url\s+"([^"]+)"\]', pictures_raw)

    def obtener_foto(indice):
        return urls[indice] if urls and len(urls) > indice else (urls[0] if urls else "")

    calle_cruda = str(row.get('Address: Street', '')).strip()
    calle = "" if calle_cruda.lower() == 'nan' else calle_cruda.split(',')[0].strip()

    colonia = str(row.get('Address: Neighborhood: Name', '')).strip()
    if colonia.lower() == 'nan': colonia = ""
    estado = str(row.get('Address: State: Name', '')).strip()
    if estado.lower() == 'nan': estado = ""
    colonia_estado = f"{colonia}, {estado}".strip(", ")

    tipo = str(row.get('Type', '')).strip()
    if tipo.lower() == 'nan': tipo = ""
    operacion = str(row.get('Listing: Operation', '')).strip()
    if operacion.lower() == 'nan': operacion = ""
    if operacion.lower() == 'sale': operacion = 'Venta'
    elif operacion.lower() == 'rent': operacion = 'Renta'

    if tipo and operacion: tipo_en_operacion = f"{tipo} en {operacion}"
    elif tipo: tipo_en_operacion = tipo
    elif operacion: tipo_en_operacion = operacion
    else: tipo_en_operacion = ""

    precio_crudo = str(row.get('Listing: Price: Price', '0')).strip()
    moneda_crudo = str(row.get('Listing: Price: Currency', 'MXN')).strip().upper()
    if moneda_crudo == 'NAN' or not moneda_crudo: moneda_crudo = "MXN"

    precio_limpio = precio_crudo.replace(',', '').replace('$', '').replace(' ', '')
    try:
        # Formato sin decimales (.00)
        precio_formateado = f"${float(precio_limpio):,.0f}"
        # Omitir MXN, solo agregar si es diferente (ej. USD)
        if moneda_crudo != "MXN":
            precio_formateado += f" {moneda_crudo}"
    except:
        precio_formateado = precio_crudo if precio_crudo.lower() != 'nan' else ""

    attr_list = []
    for val, sufijo_data in [
        (row.get('Attributes: Suites', ''), ('HABITACIÓN', 'HABITACIONES')),
        (row.get('Attributes: Bathrooms', ''), ('BAÑO', 'BAÑOS')),
        (row.get('Attributes: Toilettes', ''), ('MEDIO BAÑO', 'MEDIOS BAÑOS')),
        (row.get('Attributes: Parkings', ''), ('ESTACIONAMIENTO', 'ESTACIONAMIENTOS')),
        (row.get('Attributes: TotalSurface', ''), '<span class="normal-case lowercase">m</span>² TOTALES')
    ]:
        attr = formatear_atributo(val, sufijo_data)
        if attr: attr_list.append(attr)

    atributos_html = "".join([f"<div>{a}</div>" for a in attr_list])

    datos_propiedad = {
        "img1": url_to_base64(obtener_foto(0)), "img2": url_to_base64(obtener_foto(1)),
        "img3": url_to_base64(obtener_foto(2)), "img4": url_to_base64(obtener_foto(3)),
        "img5": url_to_base64(obtener_foto(4)), "img6": url_to_base64(obtener_foto(5)),
        "img7": url_to_base64(obtener_foto(6)), "img8": url_to_base64(obtener_foto(7)),
        "img9": url_to_base64(obtener_foto(8)), "logo": logo_b64,
        "tipo_operacion": tipo_en_operacion, "precio": precio_formateado,
        "colonia_estado": colonia_estado, "calle": calle, "atributos_html": atributos_html,
        "textura_clara": textura_clara_b64, "textura_oscura": textura_oscura_b64
    }

    return datos_propiedad, internal_id, company_clean, company_folder

# ==============================================================================
# --- 4. MOTOR DE RENDERIZADO (LOTE COMPLETO) ---
# ==============================================================================
def ejecutar_pipeline(ruta_csv):
    """Procesa un CSV completo y renderiza las imágenes."""
    print(f"📄 Procesando base de datos: {ruta_csv.name}")
    df = pd.read_csv(ruta_csv)
    imagenes_generadas = 0

    for index, row in df.iterrows():
        datos_propiedad, internal_id, company_clean, company_folder = procesar_fila_a_payload(row, textura_clara_b64, textura_oscura_b64)
        if not datos_propiedad: continue

        print(f"\nPropiedad: {internal_id}...")
        ruta_directorio = OUTPUT_DIR / company_folder / internal_id
        ruta_directorio.mkdir(parents=True, exist_ok=True)
        hti.output_path = str(ruta_directorio)

        for nombre_disenio, config in PLANTILLAS_A_GENERAR.items():
            if not config.get("activo", True): continue

            nombre_archivo = f"{internal_id}_{company_clean}_{config['sufijo_archivo']}.png"
            ruta_guardado = ruta_directorio / nombre_archivo

            if not SOBREESCRIBIR_EXISTENTES and ruta_guardado.exists():
                print(f"     ✅ El diseño {nombre_archivo} ya existe. Omitiendo...")
                continue

            print(f"  -> 🎨 Diseñando {nombre_disenio}...")
            html_final = config["funcion"](datos_propiedad)

            hti.screenshot(
                html_str=html_final,
                save_as=nombre_archivo,
                size=(config["width"], config["height"])
            )

            if config.get("cortar_carrusel"):
                print(f"     ✂️ Cortando panorámica en {config['partes']} diapositivas...")
                img_pano = Image.open(ruta_guardado)
                ancho_slide = config["width"] // config["partes"]
                alto_slide = config["height"]

                for i in range(config["partes"]):
                    corte = (i * ancho_slide, 0, (i + 1) * ancho_slide, alto_slide)
                    slide = img_pano.crop(corte)
                    nombre_slide = f"{internal_id}_{company_clean}_{config['sufijo_archivo']}_{i+1}.png"
                    slide.save(ruta_directorio / nombre_slide)

            imagenes_generadas += 1

    return imagenes_generadas

# ==============================================================================
# --- 5. EJECUCIÓN DIRECTA (solo al correr python main.py) ---
# ==============================================================================
if __name__ == "__main__":
    csv_files = sorted(DATA_DIR.glob("propiedades_1_5_10_con_fotos_*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No se encontró ningún archivo CSV en: {DATA_DIR}")

    latest_csv = csv_files[-1]
    print(f"📄 Procesando base de datos: {latest_csv.name}")

    total_imagenes = ejecutar_pipeline(latest_csv)
    print(f"\n✅ ¡Proceso terminado! Se generaron {total_imagenes} diseños en total.")
    print(f"📂 Revisa la carpeta raíz: {OUTPUT_DIR}")