import os
import sys
import django

# Define the DJANGO_SETTINGS_MODULE
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM_Comercial.settings')
django.setup()

from app.models import Prospeccao

def restore_numbers():
    print("Iniciando a restauracao dos numeros de controle...")
    
    # Para COMEX
    comex_prospeccoes = Prospeccao.objects.filter(tipo_proposta='COMEX').order_by('id')
    current_comex = 4365 # Calculado: 4749 - 385 + 1
    count_comex = 0
    for p in comex_prospeccoes:
        p.numero_controle = str(current_comex)
        p.save(update_fields=['numero_controle'])
        current_comex += 1
        count_comex += 1

    # Para PROJETO
    projeto_prospeccoes = Prospeccao.objects.filter(tipo_proposta='PROJETO').order_by('id')
    current_projeto = 410 # Calculado: 494 - 85 + 1
    count_projeto = 0
    for p in projeto_prospeccoes:
        p.numero_controle = f"PRO.{current_projeto}"
        p.save(update_fields=['numero_controle'])
        current_projeto += 1
        count_projeto += 1

    print(f"Sucesso! {count_comex} prospecções COMEX restauradas (Ultimo numero: {current_comex - 1}).")
    print(f"Sucesso! {count_projeto} prospecções PROJETO restauradas (Ultimo numero: PRO.{current_projeto - 1}).")

if __name__ == "__main__":
    restore_numbers()
