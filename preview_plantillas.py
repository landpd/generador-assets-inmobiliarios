# ==========================================
# PREVISUALIZACIÓN DE PLANTILLAS (VERSIÓN LOCAL)
# ==========================================

import importlib
import webbrowser

import mis_plantillas
from config import OUTPUT_DIR

# --- 1. Recargar las plantillas para asegurar que vemos los últimos cambios ---
importlib.reload(mis_plantillas)

# --- 2. Datos de utilería (falsos) para rellenar la plantilla ---
datos_prueba = {
    "img1": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1080&q=80",
    "img2": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1080&q=80",
    "img3": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1080&q=80",
    "img4": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1080&q=80",
    "img5": "https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=1080&q=80",
    "img6": "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=1080&q=80",
    "img7": "https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?w=1080&q=80",
    "img8": "https://images.unsplash.com/photo-1600566753086-00f18efc204b?w=1080&q=80",
    "img9": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1080&q=80",

    "logo": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_TV_2015.png",

    "tipo_operacion": "Casa en Venta",
    "precio": "$4,500,000.00 mxn",
    "colonia_estado": "Polanco, Ciudad de México",
    "calle": "Av. Presidente Masaryk 123",
    "atributos_html": "<div>3 HABITACIONES</div><div>2 BAÑOS</div><div>2 ESTACIONAMIENTOS</div><div>150 m² TOTALES</div>"
}

# =====================================================================
# 3. AQUÍ ELIGES QUÉ PLANTILLA QUIERES PREVISUALIZAR
# =====================================================================
html_generado = mis_plantillas.disenio_oferta_baja_precio(datos_prueba)

# =====================================================================
# 4. CONFIGURACIÓN DE ESCALA PARA LA VISTA PREVIA
# =====================================================================
ESCALA = 0.40

# Inyectamos el zoom con CSS directamente en el Head
html_modificado = html_generado.replace(
    '</head>',
    f'<style>body {{ zoom: {ESCALA}; margin: 0; }}</style></head>'
)

# --- 5. Guardar en OUTPUT_DIR y abrir en el navegador ---
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ruta_archivo = OUTPUT_DIR / "preview_temp.html"
ruta_archivo.write_text(html_modificado, encoding='utf-8')

print(f"📄 Preview guardado en: {ruta_archivo}")
print(f"🌐 Abriendo en el navegador...")

webbrowser.open(ruta_archivo.as_uri())
