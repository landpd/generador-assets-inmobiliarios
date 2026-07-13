import base64
import io
import random
from pathlib import Path

import requests
from PIL import Image

from config import GRAFICOS_DIR, STOCK_DIR

def cargar_textura_b64(nombre_archivo):
    ruta = GRAFICOS_DIR / nombre_archivo
    if not ruta.exists():
        return ""
    encoded = base64.b64encode(ruta.read_bytes()).decode('utf-8')
    ext = ruta.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime};base64,{encoded}"

# --- DICCIONARIO DE TEXTURAS (BASE64) ---
TEXTURAS = {
    "marco_polaroid": cargar_textura_b64("marco_polaroid.jpg"),
    "borde_roto": cargar_textura_b64("borde_roto.png"),
    "pizarra_rayones": cargar_textura_b64("pizarra_rayones.jpg"),
    "polvo_blanco": cargar_textura_b64("polvo_blanco.jpg"),
    "cristal_azul": cargar_textura_b64("cristal_azul.jpg"),
    "papel_oscuro": cargar_textura_b64("papel_oscuro.jpg"),
    "ruido_plata": cargar_textura_b64("ruido_plata.jpg"),
    "halftone_amarillo": cargar_textura_b64("halftone_amarillo.jpg")
}

# --- DICCIONARIO DE SVGS (INLINE PARA TAILWIND) ---
# Usan format() para inyectar clases de Tailwind al vuelo
SVGS = {
    "flecha_larga": '<svg class="{clases}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>',
    "casa": '<svg class="{clases}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 11.25L12 3l9.75 8.25M3 21h18M9 21v-6h6v6"/></svg>',
    "llave": '<svg class="{clases}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z"/></svg>',
    "comillas": '<svg class="{clases}" viewBox="0 0 24 24" fill="currentColor"><path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/></svg>',
    "check_circulo": '<svg class="{clases}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    "decoracion_estrellas": '<svg class="{clases}" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 7.6H22l-6.4 4.7 2.4 7.7-6.4-4.8-6.4 4.8 2.4-7.7-6.4-4.7h7.6z"/></svg>',
    "logo_pulppo_full": '<svg class="{clases}" viewBox="0 0 666 175.7" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M237.5,149.3h-4.4c-11.8,0-21.5-9.6-21.5-21.5V40.5h12.7v87.3c0,4.8,3.9,8.8,8.8,8.8h4.4v12.7ZM338.8,108.1c0,23.1-18.8,41.9-41.9,41.9s-21.6-4.5-29.2-11.9v37.5h-12.7v-67.5c0-23.1,18.8-41.9,41.9-41.9s41.9,18.8,41.9,41.9M326.1,108.1c0-16.1-13.1-29.2-29.2-29.2s-29.2,13.1-29.2,29.2,13.1,29.2,29.2,29.2,29.2-13.1,29.2-29.2M544.3,108.2c0-23.1-18.8-41.9-41.9-41.9s-41.9,18.8-41.9,41.9,18.8,41.9,41.9,41.9,41.9-18.8,41.9-41.9M531.6,108.2c0,16.1-13.1,29.2-29.2,29.2s-29.2-13.1-29.2-29.2,13.1-29.2,29.2-29.2,29.2,13.1,29.2,29.2M442.5,108.1c0,23.1-18.8,41.9-41.9,41.9s-21.6-4.5-29.2-11.9v37.5h-12.7v-67.5c0-23.1,18.8-41.9,41.9-41.9s41.9,18.8,41.9,41.9M429.8,108.1c0-16.1-13.1-29.2-29.2-29.2s-29.2,13.1-29.2,29.2,13.1,29.2,29.2,29.2,29.2-13.1,29.2-29.2M184.2,111.9v-44.5h-12.7v44.5c0,12.1-9.3,25-26.5,25s-26.5-9.3-26.5-25v-44.5h-12.7v44.5c0,10.7,3.5,20,10.2,26.8,7,7.1,17.1,10.9,29,10.9,24.6,0,39.2-19.1,39.2-37.7M83.1,108c0,22.9-18.6,41.6-41.6,41.6s-21.4-4.5-28.8-11.7v37.7H0v-67.6c0-22.9,18.7-41.5,41.5-41.5s41.6,18.6,41.6,41.5M70.4,108c0-15.9-12.9-28.8-28.8-28.8s-28.8,12.9-28.8,28.8,12.9,28.8,28.8,28.8,28.8-12.9,28.8-28.8"/><path d="M630.6,37.9c0-10.3-8.4-18.7-18.7-18.7s-18.7,8.4-18.7,18.7,1.9,9.7,5.5,13.2h0c0,0,13.2,14,13.2,14l13.2-14c3.5-3.5,5.5-8.2,5.5-13.2Z"/><path d="M612,0c-29.8,0-54,24.2-54,54s24.2,54,54,54,54-24.2,54-54S641.8,0,612,0ZM633.8,90.9c-3.7,0-7.3-1.5-9.9-4.1h0c0,0-11.8-12.6-11.8-12.6l-11.9,12.6c-2.6,2.7-6.2,4.1-9.9,4.1-7.7,0-14-6.3-14-14s6.3-14,14-14v6.2c-4.3,0-7.8,3.5-7.8,7.8s3.5,7.8,7.8,7.8,4-.8,5.5-2.3l12-12.7-13.4-14.2c-4.7-4.7-7.3-10.9-7.3-17.6,0-13.7,11.2-24.9,24.9-24.9s24.9,11.2,24.9,24.9-2.6,12.9-7.3,17.6l-13.4,14.2,12,12.7c1.5,1.5,3.4,2.3,5.5,2.3,4.3,0,7.8-3.5,7.8-7.8s-3.5-7.8-7.8-7.8v-6.2c7.7,0,14,6.3,14,14s-6.3,14-14,14Z"/></svg>',
    "logo_pulppo_isotipo": '<svg class="{clases}" viewBox="558 0 108 108" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M630.6,37.9c0-10.3-8.4-18.7-18.7-18.7s-18.7,8.4-18.7,18.7,1.9,9.7,5.5,13.2h0c0,0,13.2,14,13.2,14l13.2-14c3.5-3.5,5.5-8.2,5.5-13.2Z"/><path d="M612,0c-29.8,0-54,24.2-54,54s24.2,54,54,54,54-24.2,54-54S641.8,0,612,0ZM633.8,90.9c-3.7,0-7.3-1.5-9.9-4.1h0c0,0-11.8-12.6-11.8-12.6l-11.9,12.6c-2.6,2.7-6.2,4.1-9.9,4.1-7.7,0-14-6.3-14-14s6.3-14,14-14v6.2c-4.3,0-7.8,3.5-7.8,7.8s3.5,7.8,7.8,7.8,4-.8,5.5-2.3l12-12.7-13.4-14.2c-4.7-4.7-7.3-10.9-7.3-17.6,0-13.7,11.2-24.9,24.9-24.9s24.9,11.2,24.9,24.9-2.6,12.9-7.3,17.6l-13.4,14.2,12,12.7c1.5,1.5,3.4,2.3,5.5,2.3,4.3,0,7.8-3.5,7.8-7.8s-3.5-7.8-7.8-7.8v-6.2c7.7,0,14,6.3,14,14s-6.3,14-14,14Z"/></svg>',
    "bookmark": '<svg class="{clases}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>',
}


def obtener_foto_random_b64():
    import random
    import base64
    if not STOCK_DIR.exists():
        return ""
    # Buscar fotos en el directorio
    fotos = list(STOCK_DIR.glob('*.jpg')) + list(STOCK_DIR.glob('*.jpeg')) + list(STOCK_DIR.glob('*.png'))
    if not fotos:
        return ""

    foto_elegida = random.choice(fotos)
    try:
        encoded = base64.b64encode(foto_elegida.read_bytes()).decode('utf-8')
        ext = foto_elegida.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""


def obtener_foto_pexels_b64(api_key, collection_id):
    """
    Obtiene una foto aleatoria de una colección de Pexels.
    Fallback a obtener_foto_random_b64() si hay error de red o API.
    """
    try:
        resp = requests.get(
            f"https://api.pexels.com/v1/collections/{collection_id}",
            headers={"Authorization": api_key},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        media = data.get("media", [])
        if not media:
            return obtener_foto_random_b64()

        item = random.choice(media)
        src = item.get("src", {})
        # Prefer large, fallback a medium
        url = src.get("large") or src.get("medium") or src.get("large2x") or ""
        if not url:
            return obtener_foto_random_b64()

        img_resp = requests.get(url, timeout=20)
        img_resp.raise_for_status()

        img = Image.open(io.BytesIO(img_resp.content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

    except Exception:
        return obtener_foto_random_b64()