from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import (
    Prospeccao, AcaoProspeccao, 
    Tarefa, AcaoTarefa, 
    Servico, 
    Cliente, 
    Meta, 
    Profile
)

class Command(BaseCommand):
    help = 'Apaga todos os dados transacionais do banco de dados, exceto o superusuário.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(
            'Iniciando a limpeza de todos os dados transacionais...\n'
            'O(s) superusuário(s) e os Tipos de Serviço serão preservados.'
        ))

        # A ordem da exclusão é importante para evitar erros de Foreign Key.
        # Deletamos os "filhos" (ações) antes dos "pais" (tarefas/prospecções).

        self.stdout.write('Limpando ações de prospecção...')
        count, _ = AcaoProspeccao.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} ações de prospecção apagadas.'))

        self.stdout.write('Limpando prospecções...')
        count, _ = Prospeccao.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} prospecções apagadas.'))

        self.stdout.write('Limpando ações de tarefa...')
        count, _ = AcaoTarefa.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} ações de tarefa apagadas.'))

        self.stdout.write('Limpando tarefas...')
        count, _ = Tarefa.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} tarefas apagadas.'))

        self.stdout.write('Limpando serviços...')
        count, _ = Servico.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} serviços apagados.'))

        self.stdout.write('Limpando clientes...')
        count, _ = Cliente.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} clientes apagados.'))

        self.stdout.write('Limpando metas...')
        count, _ = Meta.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} metas apagadas.'))

        # Agora, apagamos os usuários (representantes) e seus perfis,
        # EXCLUINDO qualquer usuário que seja 'is_superuser'.
        
        self.stdout.write('Limpando perfis de representantes...')
        count, _ = Profile.objects.filter(user__is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS(f'{count} perfis de representantes apagados.'))

        self.stdout.write('Limpando usuários representantes...')
        count, _ = User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS(f'{count} usuários representantes apagados.'))

        self.stdout.write(self.style.SUCCESS(
            '\nLimpeza concluída. O banco de dados está pronto para novos testes.'
        ))