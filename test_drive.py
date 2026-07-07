# ==========================================
# SCRIPT DE PRUEBA - GOOGLE DRIVE
# ==========================================
# Ejecutar manualmente: python test_drive.py

from PIL import Image
from google_drive_manager import get_drive_service, upload_image_to_drive

# --- 1. Crear imagen de prueba (cuadro rojo 100x100px) ---
print("Creando imagen de prueba...")
img = Image.new('RGB', (100, 100), color='red')
img.save('test_image.jpg', 'JPEG')
print("Imagen guardada: test_image.jpg")

# --- 2. Conectar con Google Drive ---
print("\nConectando con Google Drive...")
service = get_drive_service()
print("Conexion exitosa.")

# --- 3. Subir imagen ---
print("\nSubiendo imagen...")
url = upload_image_to_drive(service, 'test_image.jpg')

print(f"\nExito! Archivo subido. Enlace publico: {url}")
