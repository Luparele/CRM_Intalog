import random
from datetime import date, timedelta
import calendar
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from faker import Faker

from app.models import Meta, Profile, Servico, TipoServico, User, Cliente

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste realistas desde 2020.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--representantes',
            type=int,
            help='O número de representantes a serem criados.',
            default=5
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando o povoamento massivo do banco de dados...")
        num_reps = kwargs['representantes']
        fake = Faker('pt_BR')

        # 1. Limpa dados antigos para evitar duplicatas
        self.stdout.write("Limpando dados antigos...")
        Servico.objects.all().delete()
        Meta.objects.all().delete()
        Cliente.objects.all().delete()
        TipoServico.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # 2. Cria Representantes e seus Perfis
        self.stdout.write(f"Criando {num_reps} representantes...")
        representantes = []
        for i in range(num_reps):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower().replace(' ', '')}{i}"
            user = User.objects.create_user(username=username, password='123', first_name=first_name, last_name=last_name)
            Profile.objects.create(user=user, telefone=fake.phone_number(), status='ATIVO')
            representantes.append(user)

        # 3. Cria Tipos de Serviço
        self.stdout.write("Criando tipos de serviço...")
        tipos_servico_nomes = ["Transporte Carga Fechada", "Transporte Carga Fracionada", "Armazenagem", "Logística Reversa", "Projeto Logístico"]
        tipos_servico = [TipoServico.objects.create(nome=nome) for nome in tipos_servico_nomes]

        # 4. Define o período de geração de dados
        start_date = date(2020, 1, 1)
        end_date = date(2025, 10, 4)
        total_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

        all_clientes = []

        # Loop principal para gerar dados mês a mês
        for i in range(total_months + 1):
            current_month = start_date.month + i
            current_year = start_date.year + (current_month - 1) // 12
            current_month = (current_month - 1) % 12 + 1
            
            self.stdout.write(f"Gerando dados para {calendar.month_name[current_month]}/{current_year}...")

            # Cria alguns clientes novos a cada mês
            for _ in range(random.randint(1, num_reps)):
                rep_responsavel = random.choice(representantes)
                cadastro_date = date(current_year, current_month, random.randint(1, 28))
                cliente = Cliente.objects.create(
                    cnpj=fake.cnpj(),
                    razao_social=fake.company(),
                    endereco=f"{fake.street_name()}, {random.randint(1, 2000)}",
                    nome_contato=fake.name(),
                    telefone_contato=fake.phone_number(),
                    cadastrado_por=rep_responsavel,
                )
                # Força a data de cadastro para o mês corrente do loop
                Cliente.objects.filter(pk=cliente.pk).update(data_cadastro=cadastro_date)
                all_clientes.append(cliente)
            
            # Pega uma amostra de clientes (novos e antigos) para gerar serviços
            if not all_clientes:
                continue

            clientes_do_mes = random.sample(all_clientes, min(len(all_clientes), num_reps * 2))
            
            soma_metas_individuais = Decimal('0.0')

            # Cria Serviços e Metas Individuais para cada representante
            for rep in representantes:
                # Cria meta individual para o mês
                _, ultimo_dia = calendar.monthrange(current_year, current_month)
                valor_meta_individual = Decimal(random.uniform(20000.0, 75000.0))
                soma_metas_individuais += valor_meta_individual
                Meta.objects.create(
                    tipo_meta='MENSAL_REP',
                    valor=valor_meta_individual,
                    data_inicio=date(current_year, current_month, 1),
                    data_fim=date(current_year, current_month, ultimo_dia),
                    representante=rep
                )

                # Cria serviços para este representante neste mês
                # O faturamento será algo em torno de 70% a 130% da meta dele
                faturamento_alvo_rep = valor_meta_individual * Decimal(random.uniform(0.7, 1.3))
                faturamento_gerado_rep = Decimal('0.0')

                while faturamento_gerado_rep < faturamento_alvo_rep:
                    cliente_servico = random.choice(clientes_do_mes)
                    valor_servico = Decimal(random.uniform(1500.0, 10000.0))
                    Servico.objects.create(
                        cliente=cliente_servico,
                        fechado_por=rep,
                        data_servico=date(current_year, current_month, random.randint(1, 28)),
                        valor=valor_servico,
                        tipo_servico=random.choice(tipos_servico)
                    )
                    faturamento_gerado_rep += valor_servico

            # Cria Meta Geral para o mês
            meta_geral = soma_metas_individuais * Decimal('1.2')
            Meta.objects.create(
                tipo_meta='MENSAL_GERAL',
                valor=meta_geral,
                data_inicio=date(current_year, current_month, 1),
                data_fim=date(current_year, current_month, ultimo_dia),
                representante=None
            )

        self.stdout.write(self.style.SUCCESS("Banco de dados massivamente populado com sucesso!"))