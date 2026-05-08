import os
import tarfile
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

from googleapiclient.http import MediaFileUpload
from .utils import get_drive_service

class Command(BaseCommand):
    help = 'Cria um backup compactado do projeto (excluindo venv) e envia para o Google Drive'

    def handle(self, *args, **options):

        # Configurações
        BASE_DIR = settings.BASE_DIR
        DATE_STR = datetime.datetime.now().strftime('%d-%m-%Y_as_%H-%M')
        BACKUP_FILENAME = f"CRM_Intalog_{DATE_STR}.tar.gz"
        # Configurações de Credenciais
        # Autenticação OAuth2
        try:
            service = get_drive_service()
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
            FOLDER_ID = settings.GOOGLE_DRIVE_BACKUP_FOLDER_ID
            self.stdout.write(f"Iniciando upload para o Google Drive (Pasta: {FOLDER_ID})...")

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
