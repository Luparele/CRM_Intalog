import calendar
from datetime import date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.conf import settings
from app.models import Servico, Meta, Feriado
from webpush import send_group_notification

class Command(BaseCommand):
    help = 'Envia notificações push diárias sobre o status da meta global'

    def add_arguments(self, parser):
        parser.add_argument('--test', type=str, help='Cenário de teste: success, alert, progress')

    def handle(self, *args, **options):
        test_scenario = options.get('test')
        hoje = date.today()
        mes = hoje.month
        ano = hoje.year
        
        # 1. Buscar Feriados
        feriados_datas = set(Feriado.objects.filter(data__year=ano, data__month=mes).values_list('data', flat=True))
        
        # 2. Calcular Faturamento Atual (Global)
        fat_total = Servico.objects.filter(
            data_servico__year=ano, 
            data_servico__month=mes
        ).aggregate(s=Sum('valor'))['s'] or Decimal('0.00')
        
        # 3. Calcular Meta Atual (Global)
        val_meta = Meta.objects.filter(
            mes=mes, 
            ano=ano
        ).aggregate(s=Sum('valor'))['s'] or Decimal('0.00')
        
        if val_meta <= 0 and not test_scenario:
            self.stdout.write("Nenhuma meta definida para este mês.")
            return

        # 4. Calcular Dias Úteis
        def get_dias_restantes(m, a, f):
            start_day = hoje.day
            _, last_day = calendar.monthrange(a, m)
            restantes = 0
            for d in range(start_day, last_day + 1):
                dt = date(a, m, d)
                if dt.weekday() < 5 and dt not in f:
                    restantes += 1
            return restantes

        dias_rest_uteis = get_dias_restantes(mes, ano, feriados_datas)
        hoje_is_util = (hoje.weekday() < 5 and hoje not in feriados_datas)
        
        # 5. Lógica de Mensagem (com Overrides de Teste)
        percentual = (fat_total / val_meta) * 100 if val_meta > 0 else 0
        nome_mes = calendar.month_name[mes].capitalize()
        
        # Overrides para testes
        if test_scenario == 'success':
            percentual = 100.0
            fat_total = val_meta
        elif test_scenario == 'alert':
            percentual = 95.0
            dias_rest_uteis = 1
            hoje_is_util = True
        elif test_scenario == 'progress':
            percentual = 45.0
            dias_rest_uteis = 10

        title = "CRM INTALOG - Status da Meta"
        body = ""
        
        if percentual >= 100:
            body = f"Meta Batida! Parabéns equipe Intalog! 🎉 Alcançamos {percentual:.1f}% da meta de {nome_mes}."
        elif (dias_rest_uteis == 1 and hoje_is_util) or test_scenario == 'alert':
            faltante = val_meta - fat_total
            if test_scenario == 'alert': faltante = Decimal('1500.00')
            body = f"Alerta: Hoje é o último dia útil e faltam R$ {faltante:,.2f} para a meta de {nome_mes}."
        elif percentual >= 90:
            body = f"Faltam apenas {100-percentual:.1f}% para batermos a meta de {nome_mes}! 🚀"
        else:
            body = f"Status da Meta: {percentual:.1f}% realizado. Faltam {dias_rest_uteis} dias úteis em {nome_mes}."

        # 6. Enviar Notificação
        payload = {
            "title": title,
            "body": body,
            "url": "/", # Redireciona para o dashboard
            "icon": "/static/icons/icon-192x192.png",
            "badge": "/static/icons/icon-72x72.png"
        }
        
        self.stdout.write(f"Enviando notificação ({test_scenario or 'real'}): {body}")
        
        from webpush.models import Group
        if not Group.objects.filter(name="metas").exists():
            self.stdout.write(self.style.WARNING("Ninguém se inscreveu nas notificações ainda (Grupo 'metas' não existe)."))
            return

        try:
            send_group_notification(group_name="metas", payload=payload)
            self.stdout.write(self.style.SUCCESS("Notificações enviadas com sucesso!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao disparar notificações: {e}"))
