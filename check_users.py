import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM_Comercial.settings')
sys.path.insert(0, r'C:\Users\Segurança\Documents\CRM Intalog')
django.setup()

from django.contrib.auth.models import User

print("=" * 50)
print("LISTA DE USUÁRIOS")
print("=" * 50)

for user in User.objects.all().order_by('username'):
    try:
        setor = user.profile.setor
        setor_display = user.profile.get_setor_display()
    except Exception as e:
        setor = 'ERRO'
        setor_display = str(e)
    print(f"ID: {user.id} | Username: {user.username} | Setor: {setor} ({setor_display})")

print("=" * 50)
