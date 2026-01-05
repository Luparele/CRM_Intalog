# Generated manually - Create Meta table with cliente field

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_prospeccao_tipo_proposta_and_more'),
    ]

    operations = [
        # Criar a tabela app_meta do zero com o novo schema
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.PositiveSmallIntegerField(choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')], verbose_name='Mês')),
                ('ano', models.PositiveIntegerField(verbose_name='Ano')),
                ('dias_uteis', models.PositiveIntegerField(default=22, verbose_name='Dias Úteis no Mês')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Valor da Meta (R$)')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metas', to='app.cliente', verbose_name='Cliente')),
            ],
            options={
                'ordering': ['-ano', '-mes', 'cliente'],
                'unique_together': {('cliente', 'mes', 'ano')},
            },
        ),
    ]
