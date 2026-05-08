import os
import io
import mimetypes
from django.core.files.storage import Storage
from django.conf import settings
from django.urls import reverse
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from .utils import get_drive_service

class GoogleDriveStorage(Storage):
    def __init__(self):
        self.service = get_drive_service()
        self.media_folder_id = settings.GOOGLE_DRIVE_MEDIA_FOLDER_ID

    def _get_or_create_folder(self, folder_name, parent_id):
        """Busca ou cria uma pasta no Drive."""
        query = f"name = '{folder_name}' and '{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = self.service.files().list(q=query, fields="files(id)").execute()
        files = results.get('files', [])

        if files:
            return files[0]['id']
        
        # Cria a pasta se não existir
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    def _get_folder_id_from_path(self, path):
        """Percorre o caminho e retorna o ID da pasta final."""
        parts = path.split('/')
        parent_id = self.media_folder_id
        
        # Se o caminho for apenas o nome do arquivo, retorna a pasta raiz de mídia
        if len(parts) <= 1:
            return parent_id

        # Percorre todas as pastas do caminho (exceto o último elemento, que é o arquivo)
        for folder_name in parts[:-1]:
            if folder_name:
                parent_id = self._get_or_create_folder(folder_name, parent_id)
        
        return parent_id

    def _save(self, name, content):
        """Salva o arquivo no Google Drive."""
        # Normaliza o caminho (remove barras extras e inverte se necessário no windows)
        name = name.replace('\\', '/')
        
        # Obtém o ID da pasta onde o arquivo deve ser salvo
        parent_id = self._get_folder_id_from_path(name)
        filename = os.path.basename(name)
        
        # Prepara o upload
        mime_type, _ = mimetypes.guess_type(name)
        if not mime_type:
            mime_type = 'application/octet-stream'

        media = MediaIoBaseUpload(content, mimetype=mime_type, resumable=True)
        
        file_metadata = {
            'name': filename,
            'parents': [parent_id]
        }
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        # Retornamos o 'name' original para o Django salvar no banco de dados
        return name

    def _open(self, name, mode='rb'):
        """Abre o arquivo do Google Drive (Lê o conteúdo)."""
        # Esta função é usada internamente pelo Django quando acessa .file ou .read()
        # Para otimizar, buscaremos pelo caminho
        file_id = self._get_file_id(name)
        if not file_id:
            raise FileNotFoundError(f"Arquivo não encontrado no Drive: {name}")

        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        fh.seek(0)
        return fh

    def _get_file_id(self, name):
        """Busca o ID do arquivo no Drive com base no caminho relativo."""
        name = name.replace('\\', '/')
        parts = name.split('/')
        filename = parts[-1]
        parent_id = self.media_folder_id
        
        # Se houver pastas no caminho, navega até a última
        if len(parts) > 1:
            for folder_name in parts[:-1]:
                if not folder_name: continue
                query = f"name = '{folder_name}' and '{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
                res = self.service.files().list(q=query, fields="files(id)").execute()
                files = res.get('files', [])
                if not files: return None
                parent_id = files[0]['id']

        # Busca o arquivo final na pasta encontrada
        query = f"name = '{filename}' and '{parent_id}' in parents and trashed = false"
        res = self.service.files().list(q=query, fields="files(id)").execute()
        files = res.get('files', [])
        return files[0]['id'] if files else None

    def exists(self, name):
        return self._get_file_id(name) is not None

    def url(self, name):
        """Retorna a URL customizada que passará pela nossa view de proxy."""
        # Corrigindo caminhos do Windows se existirem
        name = name.replace('\\', '/')
        return f"/media-drive/{name}"

    def size(self, name):
        file_id = self._get_file_id(name)
        if not file_id: return 0
        file = self.service.files().get(fileId=file_id, fields='size').execute()
        return int(file.get('size', 0))
