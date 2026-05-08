import os
import tarfile
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from google.oauth2 import service_account
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
        CREDENTIALS_FILE = os.path.join(BASE_DIR, 'google_credentials.json')
        
        # Tenta pegar da settings, se não existir usa placeholder
        FOLDER_ID = getattr(settings, 'GOOGLE_DRIVE_BACKUP_FOLDER_ID', None)

        if not os.path.exists(CREDENTIALS_FILE):
            self.stdout.write(self.style.ERROR(f"ERRO: Arquivo de credenciais não encontrado em: {CREDENTIALS_FILE}"))
            self.stdout.write(self.style.WARNING("Certifique-se de subir o arquivo 'google_credentials.json' para a raiz do projeto no servidor."))
            return

        if not FOLDER_ID:
            self.stdout.write(self.style.ERROR("ERRO: GOOGLE_DRIVE_BACKUP_FOLDER_ID não configurado no settings.py"))
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
                    if item in ignore_list or item == BACKUP_FILENAME or item == 'google_credentials.json':
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
            
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE, 
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
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
