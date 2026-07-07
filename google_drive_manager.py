# ==========================================
# GOOGLE DRIVE MANAGER
# ==========================================

import os
from pathlib import Path

import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes necesarios para subir archivos
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Rutas a los archivos de credenciales
BASE_DIR = Path(__file__).parent.resolve()
CREDENTIALS_JSON = BASE_DIR / "credentials.json"
TOKEN_JSON = BASE_DIR / "token.json"


def get_drive_service():
    """
    Obtiene un servicio autenticado de Google Drive.

    Si token.json existe y es válido, lo usa directamente.
    Si no existe o las credenciales son inválidas, inicia el flujo
    OAuth con credentials.json para crear un nuevo token.

    Returns:
       googleapiclient.discovery.Resource: Servicio autenticado de Drive API v3.
    """
    creds = None

    # 1. Intentar cargar credenciales existentes desde token.json
    if TOKEN_JSON.exists():
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
            str(TOKEN_JSON), SCOPES
        )

    # 2. Si no hay credenciales válidas, iniciar flujo OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refrescar token expirado
            creds.refresh(google.auth.transport.requests.Request())
        else:
            # Flujo completo de autorización
            if not CREDENTIALS_JSON.exists():
                raise FileNotFoundError(
                    f"No se encontró credentials.json en: {CREDENTIALS_JSON}\n"
                    "Descárgalo desde Google Cloud Console > APIs & Services > Credentials."
                )
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_JSON), SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Guardar el token para futuras ejecuciones
        TOKEN_JSON.write_text(creds.to_json())
        print(f"Token guardado en: {TOKEN_JSON}")

    # 3. Construir y retornar el servicio
    service = build('drive', 'v3', credentials=creds)
    return service


def upload_image_to_drive(service, file_path, folder_id=None):
    """
    Sube una imagen a Google Drive y retorna la URL pública.

    El archivo se sube a la raíz de Mi Unidad (o a la carpeta especificada)
    con permisos de lectura pública (cualquiera con el enlace puede verlo).

    Args:
        service: Servicio autenticado de Google Drive API.
        file_path (str o Path): Ruta local al archivo de imagen.
        folder_id (str, opcional): ID de la carpeta de Drive donde guardar.

    Returns:
        str: URL directa para ver la imagen en el navegador.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    # Subir archivo (a carpeta específica si se indica)
    file_metadata = {'name': file_path.name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(str(file_path), mimetype='image/jpeg')
    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
    ).execute()

    file_id = uploaded.get('id')

    # Hacer público el archivo
    service.permissions().create(
        fileId=file_id,
        body={'role': 'reader', 'type': 'anyone'},
    ).execute()

    # Construir URL directa de visualización
    url = f"https://drive.google.com/uc?export=view&id={file_id}"
    return url


def get_or_create_folder(service, folder_name="Carruseles_Metricool"):
    """
    Busca una carpeta por nombre en Google Drive. Si no existe, la crea.

    Args:
        service: Servicio autenticado de Google Drive API.
        folder_name (str): Nombre de la carpeta a buscar o crear.

    Returns:
        str: ID de la carpeta.
    """
    # Buscar si ya existe
    query = (
        f"mimeType='application/vnd.google-apps.folder' "
        f"and name='{folder_name}' and trashed=false"
    )
    response = service.files().list(
        q=query,
        fields='files(id, name)',
        pageSize=1,
    ).execute()

    folders = response.get('files', [])
    if folders:
        folder_id = folders[0]['id']
        print(f"Carpeta existente: {folder_name} ({folder_id})")
        return folder_id

    # Crear si no existe
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    created = service.files().create(
        body=folder_metadata,
        fields='id',
    ).execute()
    folder_id = created.get('id')
    print(f"Carpeta creada: {folder_name} ({folder_id})")
    return folder_id
