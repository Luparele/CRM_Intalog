import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Prospeccao, AcaoProspeccao, Cliente, User

class Command(BaseCommand):
    help = 'Popula a tabela de Prospecção com dados de teste.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando o povoamento da tabela de prospecções...'))

        # Busca usuários e clientes existentes
        usuarios = list(User.objects.filter(is_active=True))
        clientes = list(Cliente.objects.all())

        if not usuarios or not clientes:
            self.stdout.write(self.style.ERROR('Nenhum usuário ativo ou cliente encontrado. Cancele a operação.'))
            return

        # Limpa dados antigos para evitar duplicatas
        AcaoProspeccao.objects.all().delete()
        Prospeccao.objects.all().delete()
        self.stdout.write(self.style.WARNING('Tabelas AcaoProspeccao e Prospeccao limpas.'))

        start_date = timezone.datetime(2020, 1, 1, tzinfo=timezone.get_current_timezone())
        end_date = timezone.now()
        total_days = (end_date - start_date).days

        # Gera entre 150 e 250 prospecções no total
        num_prospeccoes = random.randint(150, 250)

        for i in range(num_prospeccoes):
            # Define uma data de criação aleatória no período
            dias_aleatorios = random.randint(0, total_days)
            data_criacao = start_date + timedelta(days=dias_aleatorios)

            # Sorteia um status
            status_final = random.choices(
                ['FECHADO', 'DESISTENCIA', 'PERDIDA'], weights=[50, 25, 25], k=1
            )[0]
            status = random.choices(
                ['NOVA', 'NEGOCIANDO', status_final], weights=[15, 35, 50], k=1
            )[0]
            
            # Sorteia outros dados
            cliente_aleatorio = random.choice(clientes)
            criado_por_aleatorio = random.choice(usuarios)
            tipo_proposta = random.choice([c[0] for c in Prospeccao.TIPO_PROPOSTA_CHOICES])
            viagens = random.randint(1, 50)
            valor_viagem = random.uniform(500.0, 7500.0)
            
            # Cria a prospecção
            prospeccao = Prospeccao.objects.create(
                cliente=cliente_aleatorio,
                criado_por=criado_por_aleatorio,
                data_criacao=data_criacao,
                tipo_proposta=tipo_proposta,
                duracao_meses=random.randint(1, 24),
                viagens_aproximadas=viagens,
                valor_medio_viagem=round(valor_viagem, 2),
                valor_total=round(viagens * valor_viagem, 2),
                status=status
            )
            
            # Adiciona dados de início e finalização se aplicável
            if status != 'NOVA':
                prospeccao.data_inicio_negociacao = data_criacao + timedelta(days=random.randint(1, 15))
                prospeccao.iniciado_por = criado_por_aleatorio
                
                # Adiciona ações
                for _ in range(random.randint(1, 5)):
                    AcaoProspeccao.objects.create(
                        prospeccao=prospeccao,
                        descricao=random.choice([
                            "Contato inicial realizado com o cliente.",
                            "Enviado e-mail com apresentação da proposta.",
                            "Reunião agendada para discutir detalhes.",
                            "Cliente solicitou ajuste no valor.",
                            "Aguardando retorno do setor de compras."
                        ]),
                        registrado_por=criado_por_aleatorio,
                        data_registro=prospeccao.data_inicio_negociacao + timedelta(days=random.randint(1, 10))
                    )
                
                if status in ['FECHADO', 'DESISTENCIA', 'PERDIDA']:
                    prospeccao.data_finalizacao = prospeccao.data_inicio_negociacao + timedelta(days=random.randint(5, 45))
                    prospeccao.finalizado_por = criado_por_aleatorio
                    
                    # Adiciona a ação de finalização
                    desc_final = {
                        'FECHADO': "Prospecção finalizada: Serviço Fechado.",
                        'DESISTENCIA': "Prospecção finalizada: Desistência do Cliente.",
                        'PERDIDA': "Prospecção finalizada: Negociação Perdida."
                    }
                    AcaoProspeccao.objects.create(
                        prospeccao=prospeccao,
                        descricao=desc_final[status],
                        registrado_por=criado_por_aleatorio,
                        data_registro=prospeccao.data_finalizacao
                    )
            
            prospeccao.save()
            self.stdout.write(f'  -> Prospecção {i+1}/{num_prospeccoes} criada para {cliente_aleatorio.razao_social}')

        self.stdout.write(self.style.SUCCESS('Povoamento concluído com sucesso!'))