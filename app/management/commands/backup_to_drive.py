import os
import tarfile
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GOOGLE_LIBS_INSTALLED = True
except ImportError:
    GOOGLE_LIBS_INSTALLED = False

class Command(BaseCommand):
    help = 'Cria um backup compactado do projeto (excluindo venv) e envia para o Google Drive'

    def handle(self, *args, **options):
        if not GOOGLE_LIBS_INSTALLED:
            self.stdout.write(self.style.ERROR("As bibliotecas do Google não estão instaladas. Execute: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"))
            return

        # Configurações
        BASE_DIR = settings.BASE_DIR
        DATE_STR = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        BACKUP_FILENAME = f"backup_crm_{DATE_STR}.tar.gz"
        # Configurações de Credenciais
        TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')
        CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')
        FOLDER_ID = getattr(settings, 'GOOGLE_DRIVE_BACKUP_FOLDER_ID', None)

        if not os.path.exists(TOKEN_FILE):
            self.stdout.write(self.style.ERROR(f"ERRO: Arquivo 'token.json' não encontrado em: {TOKEN_FILE}"))
            return

        if not FOLDER_ID:
            self.stdout.write(self.style.ERROR("ERRO: GOOGLE_DRIVE_BACKUP_FOLDER_ID não configurado no settings.py"))
            return

        # Autenticação OAuth2
        creds = None
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=['https://www.googleapis.com/auth/drive.file'])
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    self.stdout.write("Token expirado. Tentando renovar...")
                    creds.refresh(Request())
                    # Salva o token renovado
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())
                    self.stdout.write(self.style.SUCCESS("Token renovado com sucesso!"))
                else:
                    self.stdout.write(self.style.ERROR("Token inválido ou sem permissão de renovação."))
                    return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro na autenticação: {e}"))
            return

        # 1. Criar o Backup (Compactar)
        self.stdout.write(f"Iniciando compactação em {BACKUP_FILENAME}...")
        try:
            # Pastas a ignorar
            ignore_list = [
                'venv', '.git', '__pycache__', 'static_root', 
                'Backup', '.gemini', 'node_modules', '.venv'
            ]
            
            with tarfile.open(BACKUP_FILENAME, "w:gz") as tar:
                for item in os.listdir(BASE_DIR):
                    if item in ignore_list or item == BACKUP_FILENAME or item in ['token.json', 'client_secrets.json', 'google_credentials.json']:
                        continue
                    
                    item_path = os.path.join(BASE_DIR, item)
                    self.stdout.write(f"  Adicionando: {item}...")
                    tar.add(item_path, arcname=item)
            
            self.stdout.write(self.style.SUCCESS(f"Backup compactado com sucesso!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha ao criar arquivo de backup: {e}"))
            return

        # 2. Upload para o Google Drive
        try:
            self.stdout.write(f"Iniciando upload para o Google Drive (Pasta: {FOLDER_ID})...")
            
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {
                'name': BACKUP_FILENAME,
                'parents': [FOLDER_ID]
            }
            media = MediaFileUpload(
                BACKUP_FILENAME, 
                mimetype='application/gzip', 
                resumable=True
            )
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()

            self.stdout.write(self.style.SUCCESS(f"Backup enviado com sucesso! Google Drive File ID: {file.get('id')}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro durante o upload para o Google Drive: {e}"))
        finally:
            # 3. Limpeza do arquivo temporário
            if os.path.exists(BACKUP_FILENAME):
                os.remove(BACKUP_FILENAME)
                self.stdout.write("Arquivo temporário de backup removido do servidor.")
