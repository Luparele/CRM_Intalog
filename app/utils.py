import os
from django.conf import settings
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_drive_service():
    """
    Retorna um serviço autenticado da API do Google Drive (v3).
    Utiliza token.json e client_secrets.json na raiz do projeto.
    """
    BASE_DIR = settings.BASE_DIR
    TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')
    
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"Arquivo 'token.json' não encontrado em: {TOKEN_FILE}")

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=['https://www.googleapis.com/auth/drive.file'])
    
    # Verifica/Renova o token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        else:
            raise Exception("Token inválido ou expirado sem refresh_token.")

    return build('drive', 'v3', credentials=creds)
