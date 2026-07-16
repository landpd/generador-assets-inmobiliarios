# =========================================
# CELDA 02 - GENERADOR DE PROMTS CON GEMINI
# =========================================

import re
import time
import google.generativeai as genai

from utils import formatear_atributo

# --- ACTUALIZACIÓN DE MODELO ---
model = genai.GenerativeModel('gemini-3.1-flash-lite')

# --- FUNCIONES DE AYUDA ---
def obtener_emoji_propiedad(tipo_str):
    t = tipo_str.lower()
    if 'condominio' in t: return '🏘️'
    elif 'casa' in t: return '🏠'
    elif 'departamento' in t or 'apartment' in t: return '🏬'
    elif 'terreno' in t or 'land' in t or 'lote' in t: return '🏗️'
    elif 'oficina' in t: return '🏢'
    elif 'local' in t: return '🏪'
    else: return '📍'

# --- PROCESAMIENTO PRINCIPAL ---
datos_metricool = []

print(f"🤖 Generando copys usando Gemini 3.1 Flash Lite (Respetando límite de 15 RPM)...\n")

for item in propiedades_listas_para_publicar:
    row = item["datos_ficha"]
    rutas_imagenes = item["rutas_imagenes"]

    internal_id = str(row.get('InternalId', '')).strip()

    # --- TEXTOS Y UBICACIÓN ---
    colonia = str(row.get('Address: Neighborhood: Name', '')).strip()
    if colonia.lower() == 'nan': colonia = ""
    estado = str(row.get('Address: State: Name', '')).strip()
    if estado.lower() == 'nan': estado = ""

    if colonia and estado:
        colonia_estado = f"{colonia}, {estado}"
    else:
        colonia_estado = colonia or estado

    # --- LÓGICA: TIPO Y OPERACIÓN ---
    tipo = str(row.get('Type', '')).strip()
    if tipo.lower() == 'nan': tipo = ""
    operacion = str(row.get('Listing: Operation', '')).strip()
    if operacion.lower() == 'nan': operacion = ""

    if operacion.lower() == 'sale': operacion = 'Venta'
    elif operacion.lower() == 'rent': operacion = 'Renta'

    if tipo and operacion:
        tipo_en_operacion = f"{tipo} en {operacion}"
    elif tipo:
        tipo_en_operacion = tipo
    elif operacion:
        tipo_en_operacion = operacion
    else:
        tipo_en_operacion = "Propiedad"

    emoji_tipo = obtener_emoji_propiedad(tipo)

    # --- TÍTULO PARA FACEBOOK Y TIKTOK ---
    titulo_publicacion = f"{tipo_en_operacion} en {colonia_estado}"

    # --- LÓGICA: PRECIO ---
    precio_crudo = str(row.get('Listing: Price: Price', '0')).strip()
    moneda_crudo = str(row.get('Listing: Price: Currency', 'mxn')).strip().lower()
    if moneda_crudo == 'nan' or moneda_crudo == '': moneda_crudo = "mxn"
    precio_limpio = precio_crudo.replace(',', '').replace('$', '').replace(' ', '')

    try:
        precio_formateado = f"${float(precio_limpio):,.2f} {moneda_crudo}"
    except:
        precio_formateado = precio_crudo if precio_crudo.lower() != 'nan' else ""

    # --- LÓGICA: ATRIBUTOS CON EMOJIS ---
    attr_list = []
    config_atributos = [
        (row.get('Attributes: Suites', ''), ('Habitación', 'Habitaciones'), '🛏️'),
        (row.get('Attributes: Bathrooms', ''), ('Baño', 'Baños'), '🛁'),
        (row.get('Attributes: Parkings', ''), ('Estacionamiento', 'Estacionamientos'), '🚗'),
        (row.get('Attributes: TotalSurface', ''), 'm² Totales', '📐')
    ]

    for val, sufijo_data, emoji_attr in config_atributos:
        attr_texto = formatear_atributo(val, sufijo_data)
        if attr_texto:
            attr_list.append(f"{emoji_attr} {attr_texto}")

    atributos_finales = "\n".join(attr_list)

    # --- GENERACIÓN IA ---
    descripcion_original = str(row.get('Listing: Description', '')).strip()

    prompt_ia = f"""
    Actúa como un experto copywriter inmobiliario.
    Aquí tienes la descripción original de una propiedad en {colonia_estado}:
    "{descripcion_original}"

    Tu tarea: Genera un texto persuasivo muy breve (máximo 1 o 2 líneas) destacando el PRINCIPAL beneficio de esta propiedad.
    IMPORTANTE:
    - NO incluyas saludos ni despedidas.
    - NO uses emojis (ya los pondré yo).
    - NO uses hashtags.
    - Ve directo al grano.
    """

    try:
        respuesta_ia = model.generate_content(prompt_ia)
        texto_beneficio = respuesta_ia.text.strip()
    except Exception as e:
        print(f"⚠️ Error con Gemini en {internal_id}: {e}")
        texto_beneficio = "Una excelente oportunidad que no puedes dejar pasar por su gran ubicación y espacios."

    time.sleep(4.5) # Pausa de seguridad API

    # --- ENSAMBLAJE DEL TEXTO FINAL (COPY) ---
    copy_final = f"{emoji_tipo} {tipo_en_operacion} en 📍 {colonia_estado}.\n"
    copy_final += f"{texto_beneficio}\n"
    if atributos_finales:
        copy_final += f"{atributos_finales}\n"
    if precio_formateado:
        copy_final += f"💰 {precio_formateado}\n"
    copy_final += f"📩 Agenda tu visita y contáctanos para más información.\n"
    copy_final += f"[{internal_id}]"

    # --- ENSAMBLAJE DEL PRIMER COMENTARIO ---
    id_largo = str(row.get('ID', '')).strip()
    enlace_pulppo = f"https://pulppo.com/{id_largo}"
    primer_comentario = f"Conoce todos los detalles de esta propiedad haciendo clic en este enlace: {enlace_pulppo}"

    # --- GUARDAR PARA EL CSV FINAL ---
    datos_metricool.append({
        "internal_id": internal_id,
        "copy_final": copy_final,
        "primer_comentario": primer_comentario,
        "rutas_imagenes_locales": rutas_imagenes,
        "titulo_publicacion": titulo_publicacion # <--- SE AGREGÓ PARA USAR EN FB Y TIKTOK
    })

    print(f"✅ Copy generado exitosamente para: {internal_id}")

print("\n🎉 ¡Todos los textos han sido generados y empaquetados!")