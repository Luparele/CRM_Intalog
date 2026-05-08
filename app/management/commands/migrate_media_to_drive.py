import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
from app.storage import GoogleDriveStorage

class Command(BaseCommand):
    help = 'Migra os arquivos da pasta /media/ local para o Google Drive'

    def handle(self, *args, **options):
        # Verifica se o storage atual é o do Google Drive
        if not isinstance(default_storage, GoogleDriveStorage):
            self.stdout.write(self.style.ERROR("O storage padrão não é GoogleDriveStorage. Verifique seu settings.py"))
            return

        MEDIA_ROOT = settings.MEDIA_ROOT
        if not os.path.exists(MEDIA_ROOT):
            self.stdout.write(self.style.WARNING(f"Pasta MEDIA_ROOT não encontrada: {MEDIA_ROOT}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Iniciando migração de: {MEDIA_ROOT}"))

        count = 0
        errors = 0

        # Percorre recursivamente a pasta media
        for root, dirs, files in os.walk(MEDIA_ROOT):
            for filename in files:
                # Caminho completo no disco
                local_path = os.path.join(root, filename)
                
                # Caminho relativo para o Django (ex: tarefas/foto.jpg)
                relative_path = os.path.relpath(local_path, MEDIA_ROOT).replace('\\', '/')

                if default_storage.exists(relative_path):
                    self.stdout.write(self.style.WARNING(f"  [PULADO] Já existe no Drive: {relative_path}"))
                    continue

                self.stdout.write(f"  [MIGRANDO] {relative_path}...")
                
                try:
                    with open(local_path, 'rb') as f:
                        django_file = File(f)
                        default_storage.save(relative_path, django_file)
                    
                    self.stdout.write(self.style.SUCCESS(f"    OK!"))
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ERRO ao migrar {relative_path}: {e}"))
                    errors += 1

        self.stdout.write(self.style.SUCCESS(f"\nMigração concluída!"))
        self.stdout.write(f"Arquivos migrados: {count}")
        self.stdout.write(f"Erros encontrados: {errors}")
        self.stdout.write(self.style.WARNING("\nIMPORTANTE: Os arquivos locais NÃO foram apagados. Verifique se estão no Drive antes de remover a pasta /media/ do servidor."))
