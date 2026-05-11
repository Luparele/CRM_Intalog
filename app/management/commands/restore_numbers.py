from django.core.management.base import BaseCommand
from app.models import Prospeccao

class Command(BaseCommand):
    help = 'Restaura os números de controle perdidos nas prospecções com base na ordem de criação'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando a restauracao dos numeros de controle...")
        
        # Para COMEX
        comex_prospeccoes = Prospeccao.objects.filter(tipo_proposta='COMEX').order_by('id')
        current_comex = 4365 # Calculado para bater com 4749
        count_comex = 0
        for p in comex_prospeccoes:
            p.numero_controle = str(current_comex)
            p.save(update_fields=['numero_controle'])
            current_comex += 1
            count_comex += 1

        # Para PROJETO
        projeto_prospeccoes = Prospeccao.objects.filter(tipo_proposta='PROJETO').order_by('id')
        current_projeto = 410 # Calculado para bater com PRO.494
        count_projeto = 0
        for p in projeto_prospeccoes:
            p.numero_controle = f"PRO.{current_projeto}"
            p.save(update_fields=['numero_controle'])
            current_projeto += 1
            count_projeto += 1

        self.stdout.write(self.style.SUCCESS(f"Sucesso! {count_comex} prospecções COMEX restauradas (Último número: {current_comex - 1})."))
        self.stdout.write(self.style.SUCCESS(f"Sucesso! {count_projeto} prospecções PROJETO restauradas (Último número: PRO.{current_projeto - 1})."))
