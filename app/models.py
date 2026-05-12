from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class TipoServico(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Serviço")

    def __str__(self):
        return self.nome

class Profile(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]
    
    # --- ALTERAÇÃO: REMOVIDO FINANCEIRO ---
    SETOR_CHOICES = [
        ('REPRESENTANTE', 'Representante Comercial'),
        ('COMERCIAL', 'Diretoria Comercial'),
        ('GERENTE', 'Gerente Operacional'),
        ('DIRETORIA', 'Diretoria'),
        ('ADMIN', 'Administrativo (TI/Sistema)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    eh_representante = models.BooleanField(default=False, verbose_name="É Representante Comercial?")
    
    setor = models.CharField(
        max_length=20,
        choices=SETOR_CHOICES,
        default='REPRESENTANTE',
        verbose_name="Setor / Função"
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')
    
    def __str__(self):
        return f"{self.user.username} ({self.get_setor_display()})"
    
    @property
    def is_representante(self):
        return self.setor == 'REPRESENTANTE'
    
    @property
    def is_gerente_operacional(self):
        return self.setor == 'GERENTE'

    @property
    def is_comercial(self):
        return self.setor == 'COMERCIAL'
    
    @property
    def is_diretoria(self):
        return self.setor == 'DIRETORIA'
    
    @property
    def is_admin_sistema(self):
        return self.setor == 'ADMIN'
        
    @property
    def tem_acesso_gestao(self):
        """
        Acesso total (criar/editar/excluir):
        - COMERCIAL (Diretoria Comercial)
        - ADMIN (Administrativo/TI)
        """
        return self.setor in ['COMERCIAL', 'ADMIN']
    
    @property
    def tem_acesso_visualizacao_geral(self):
        """
        Pode visualizar dados de todos (mas não editar):
        - DIRETORIA
        - GERENTE (Gerente Operacional)
        """
        return self.setor in ['DIRETORIA', 'GERENTE']
    
    @property
    def pode_acessar_agenda(self):
        """Agenda: REPRESENTANTE, DIRETORIA, COMERCIAL, ADMIN"""
        return self.setor in ['REPRESENTANTE', 'DIRETORIA', 'COMERCIAL', 'ADMIN']
    
    @property
    def pode_acessar_prospeccao(self):
        """Prospecção: REPRESENTANTE, DIRETORIA (view), COMERCIAL, ADMIN"""
        return self.setor in ['REPRESENTANTE', 'DIRETORIA', 'COMERCIAL', 'ADMIN']
    
    @property
    def pode_acessar_clientes(self):
        """Clientes: REPRESENTANTE (seus), COMERCIAL, DIRETORIA (view), ADMIN"""
        return self.setor in ['REPRESENTANTE', 'COMERCIAL', 'DIRETORIA', 'ADMIN']
    
    @property
    def pode_acessar_usuarios(self):
        """Usuários: REPRESENTANTE (próprio), COMERCIAL, DIRETORIA (view), ADMIN"""
        return self.setor in ['REPRESENTANTE', 'COMERCIAL', 'DIRETORIA', 'ADMIN']
    
    @property
    def pode_acessar_metas(self):
        """Metas: COMERCIAL, DIRETORIA (view), ADMIN"""
        return self.setor in ['COMERCIAL', 'DIRETORIA', 'ADMIN']

class Cliente(models.Model):
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ") 
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    nome_contato = models.CharField(max_length=100, verbose_name="Nome do Contato")
    telefone_contato = models.CharField(max_length=20, verbose_name="Telefone do Contato")
    
    cadastrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clientes_cadastrados',
        verbose_name="Cadastrado Por"
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    
    def __str__(self):
        return self.razao_social

class ClienteProspect(models.Model):
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", blank=True, null=True)
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social / Nome")
    nome_contato = models.CharField(max_length=100, verbose_name="Nome do Contato")
    telefone_contato = models.CharField(max_length=20, verbose_name="Telefone do Contato")
    email_contato = models.EmailField(max_length=100, verbose_name="E-mail", blank=True, null=True)
    
    cadastrado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='prospects_cadastrados',
        verbose_name="Cadastrado Por"
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    
    # Campos para controle de promoção a cliente ativo
    promovido = models.BooleanField(default=False, verbose_name="Promovido a Cliente")
    data_promocao = models.DateTimeField(null=True, blank=True, verbose_name="Data da Promoção")
    cliente_ativo = models.ForeignKey(
        'Cliente', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='prospect_origem',
        verbose_name="Cliente Ativo Gerado"
    )

    def __str__(self):
        return f"{self.razao_social} (Prospect)"

class Servico(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='servicos',
        verbose_name="Cliente"
    )
    fechado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='servicos_fechados',
        verbose_name="Fechado Por"
    )
    data_servico = models.DateField(verbose_name="Data do Serviço")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade de Viagens")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    
    tipo_servico = models.ForeignKey(
        'TipoServico',
        on_delete=models.PROTECT,
        verbose_name="Tipo de Serviço",
        null=True,
        blank=True
    )
    
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    def __str__(self):
        tipo_servico_nome = self.tipo_servico.nome if self.tipo_servico else "Sem tipo"
        return f"{tipo_servico_nome} para {self.cliente.razao_social}"

class Meta(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='metas',
        verbose_name="Cliente"
    )
    
    mes = models.PositiveSmallIntegerField(verbose_name="Mês Base")
    ano = models.PositiveIntegerField(verbose_name="Ano Base")
    dias_uteis = models.PositiveIntegerField(verbose_name="Dias Úteis", default=22)
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Meta a ser alcançada (R$)")

    class Meta:
        ordering = ['-ano', '-mes', 'cliente']
        unique_together = ('cliente', 'mes', 'ano')

    def __str__(self):
        return f"{self.cliente.razao_social} - {self.mes}/{self.ano}"

class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('NAO_INICIADA', 'Pendente'),
        ('INICIADA', 'Iniciada'), # Mantendo para legado
        ('FINALIZADA', 'Finalizada'), # Mantendo para legado
        ('REALIZADA', 'Realizada'),
        ('NAO_REALIZADA', 'Não Realizada'),
    ]
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NAO_INICIADA')
    
    criado_por = models.ForeignKey(User, related_name='tarefas_criadas', on_delete=models.PROTECT, verbose_name="Criado por")
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Criação")
    
    iniciado_por = models.ForeignKey(User, related_name='tarefas_iniciadas', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Iniciado por")
    data_inicio = models.DateTimeField(null=True, blank=True, verbose_name="Data de Início")
    
    finalizado_por = models.ForeignKey(User, related_name='tarefas_finalizadas', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Finalizado por")
    data_finalizacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Finalização")

    # Novos campos para funcionalidade de Tarefas/Agenda
    atribuido_a = models.ForeignKey(User, related_name='tarefas_atribuidas', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Atribuído a")
    data_agendamento = models.DateField(null=True, blank=True, verbose_name="Data Agendamento")
    visualizada_em = models.DateTimeField(null=True, blank=True, verbose_name="Visualizada em")

    def __str__(self):
        return self.titulo


class TarefaAgendada(models.Model):
    """
    Nova tabela para a página Tarefas (independente da Agenda antiga).
    """
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('REALIZADA', 'Realizada'),
        ('NAO_REALIZADA', 'Não Realizada'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    data_agendamento = models.DateField(verbose_name="Data Agendamento")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    atribuido_a = models.ForeignKey(User, related_name='tarefas_agendadas_atribuidas', on_delete=models.CASCADE, verbose_name="Atribuído a")
    criado_por = models.ForeignKey(User, related_name='tarefas_agendadas_criadas', on_delete=models.CASCADE, verbose_name="Criado por")
    visualizada_em = models.DateTimeField(null=True, blank=True, verbose_name="Visualizada em")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    finalizado_por = models.ForeignKey(User, related_name='tarefas_agendadas_finalizadas', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.data_agendamento}"

    def get_responsavel_nome(self):
        if self.atribuido_a:
            return self.atribuido_a.get_full_name() or self.atribuido_a.username
        return "-Sem Atribuição-"

    def get_finalizador_nome(self):
        if self.finalizado_por:
            return self.finalizado_por.get_full_name() or self.finalizado_por.username
        return "-"


class AcaoTarefa(models.Model):
    tarefa = models.ForeignKey(Tarefa, related_name='acoes', on_delete=models.CASCADE, verbose_name="Tarefa")
    descricao = models.TextField(verbose_name="Descrição da Ação")
    
    arquivo = models.FileField(
        upload_to='uploads/tarefas/%Y/%m/', 
        null=True, 
        blank=True, 
        verbose_name="Arquivo Anexo"
    )
    
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Registrado por")
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de Registro")

    class Meta:
        ordering = ['data_registro']

    def __str__(self):
        return f'Ação em "{self.tarefa.titulo}" por {self.registrado_por.username}'

class Prospeccao(models.Model):
    STATUS_CHOICES = [
        ('NOVA', 'Nova'),
        ('NEGOCIANDO', 'Em Negociação'),
        ('FECHADO', 'Serviço Fechado'),
        ('DESISTENCIA', 'Desistência do Cliente'),
        ('PERDIDA', 'Negociação Perdida'),
    ]

    TIPO_PROPOSTA_CHOICES = [
        ('COMEX', 'COMEX/DOMESTIC'),
        ('PROJETO', 'PROJETO'),
    ]

    cliente = models.ForeignKey(ClienteProspect, on_delete=models.CASCADE, related_name='prospeccoes')
    
    numero_controle = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Numero de Controle')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOVA')

    tipo_proposta = models.CharField(
        max_length=20, 
        choices=TIPO_PROPOSTA_CHOICES, 
        default='COMEX',
        verbose_name="Tipo de Proposta"
    )
    
    tipo_servico = models.ForeignKey(
        'TipoServico',
        on_delete=models.PROTECT,
        verbose_name="Tipo de Serviço",
        null=True,
        blank=False
    )
    duracao_meses = models.PositiveIntegerField(verbose_name="Duração em Meses (Aprox.)")
    viagens_aproximadas = models.PositiveIntegerField(verbose_name="Nº de Viagens (Aprox.)")
    valor_medio_viagem = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Médio por Viagem")
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total Estimado")

    criado_por = models.ForeignKey(User, related_name='prospeccoes_criadas', on_delete=models.PROTECT)
    atribuido_a = models.ForeignKey(
        User, 
        related_name='prospeccoes_atribuidas', 
        on_delete=models.PROTECT,
        null=True, 
        blank=True,
        verbose_name="Atribuído a"
    )
    data_criacao = models.DateTimeField(default=timezone.now)
    
    iniciado_por = models.ForeignKey(User, related_name='prospeccoes_iniciadas', on_delete=models.PROTECT, null=True, blank=True)
    data_inicio_negociacao = models.DateTimeField(null=True, blank=True)
    
    finalizado_por = models.ForeignKey(User, related_name='prospeccoes_finalizadas', on_delete=models.PROTECT, null=True, blank=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    @property
    def dias_na_etapa(self):
        hoje = timezone.now().date()
        if self.status == 'NOVA':
            delta = hoje - self.data_criacao.date()
            return delta.days
        elif self.status == 'NEGOCIANDO' and self.data_inicio_negociacao:
            delta = hoje - self.data_inicio_negociacao.date()
            return delta.days
        return None


    def save(self, *args, **kwargs):
        # Gerar numero_controle automaticamente se nao existir
        if not self.numero_controle:
            # Lógica para COMEX/DOMESTIC
            if self.tipo_proposta == 'COMEX':
                # Busca o maior número que NÃO começa com "PRO."
                ultima = Prospeccao.objects.filter(
                    tipo_proposta='COMEX',
                    numero_controle__isnull=False
                ).exclude(
                    numero_controle__startswith='PRO.'
                ).order_by('-id').first() # Ordena por ID ou extração numérica seria ideal, mas por ID é proxy razoavel para sequencia temporal

                if ultima and ultima.numero_controle.isdigit():
                    proximo = int(ultima.numero_controle) + 1
                    if proximo < 4889:
                        proximo = 4889
                else:
                    proximo = 4889 # Inicial solicitado
                
                self.numero_controle = str(proximo)

            # Lógica para PROJETO
            elif self.tipo_proposta == 'PROJETO':
                # Busca o maior número que COMEÇA com "PRO."
                ultima = Prospeccao.objects.filter(
                    tipo_proposta='PROJETO',
                    numero_controle__startswith='PRO.'
                ).order_by('-id').first()

                if ultima:
                    try:
                        # Extrai o numero apos "PRO."
                        ultimo_num = int(ultima.numero_controle.split('.')[-1])
                        proximo = ultimo_num + 1
                        if proximo < 511:
                            proximo = 511
                    except ValueError:
                         proximo = 511
                else:
                    proximo = 511 # Inicial solicitado
                
                self.numero_controle = f"PRO.{proximo}"
        
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Prospecção para {self.cliente.razao_social} ({self.get_status_display()})"

class AcaoProspeccao(models.Model):
    prospeccao = models.ForeignKey(Prospeccao, related_name='acoes', on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name="Descrição da Ação")
    
    arquivo = models.FileField(
        upload_to='uploads/prospeccao/%Y/%m/', 
        null=True, 
        blank=True, 
        verbose_name="Arquivo Anexo"
    )
    
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['data_registro']

    def __str__(self):
        return f'Ação em "{self.prospeccao.cliente.razao_social}" por {self.registrado_por.username}'

class Feriado(models.Model):
    data = models.DateField(unique=True, verbose_name="Data do Feriado")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")

    class Meta:
        ordering = ['data']
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y')} - {self.descricao}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
