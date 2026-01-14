from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Cliente, ClienteProspect, Servico, TipoServico, 
    Meta, Tarefa, AcaoTarefa, Prospeccao, AcaoProspeccao
)


# ===== USER & PROFILE =====

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para o perfil do usuário"""
    class Meta:
        model = Profile
        fields = ['setor', 'tem_acesso_gestao']
        read_only_fields = ['setor', 'tem_acesso_gestao']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuários/representantes"""
    profile = ProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'full_name', 'is_active', 'profile']
        read_only_fields = ['id', 'username']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuários"""
    password = serializers.CharField(write_only=True, required=True)
    setor = serializers.ChoiceField(
        choices=Profile.SETOR_CHOICES,
        write_only=True,
        required=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'password', 'setor']
    
    def create(self, validated_data):
        setor = validated_data.pop('setor')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, setor=setor)
        return user


# ===== CLIENTES =====

class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para clientes ativos"""
    cadastrado_por_nome = serializers.CharField(
        source='cadastrado_por.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'cnpj', 'razao_social', 'endereco', 
            'nome_contato', 'telefone_contato',
            'data_cadastro', 'cadastrado_por', 'cadastrado_por_nome'
        ]
        read_only_fields = ['id', 'data_cadastro']


class ClienteProspectSerializer(serializers.ModelSerializer):
    """Serializer para clientes em prospecção"""
    cadastrado_por_nome = serializers.CharField(
        source='cadastrado_por.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = ClienteProspect
        fields = [
            'id', 'cnpj', 'razao_social', 'nome_contato',
            'telefone_contato', 'data_cadastro', 
            'cadastrado_por', 'cadastrado_por_nome'
        ]
        read_only_fields = ['id', 'data_cadastro']


# ===== SERVIÇOS =====

class TipoServicoSerializer(serializers.ModelSerializer):
    """Serializer para tipos de serviço"""
    class Meta:
        model = TipoServico
        fields = ['id', 'nome']
        read_only_fields = ['id']


class ServicoSerializer(serializers.ModelSerializer):
    """Serializer para serviços/transportes realizados"""
    cliente_razao_social = serializers.CharField(
        source='cliente.razao_social',
        read_only=True
    )
    tipo_servico_nome = serializers.CharField(
        source='tipo_servico.nome',
        read_only=True
    )
    fechado_por_nome = serializers.CharField(
        source='fechado_por.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = Servico
        fields = [
            'id', 'cliente', 'cliente_razao_social',
            'tipo_servico', 'tipo_servico_nome',
            'data_servico', 'quantidade', 'valor',
            'data_registro', 'fechado_por', 'fechado_por_nome'
        ]
        read_only_fields = ['id', 'data_registro', 'fechado_por']


class ServicoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de serviços"""
    class Meta:
        model = Servico
        fields = ['cliente', 'tipo_servico', 'data_servico', 'quantidade', 'valor']


# ===== METAS =====

class MetaSerializer(serializers.ModelSerializer):
    """Serializer para metas mensais por cliente"""
    cliente_razao_social = serializers.CharField(
        source='cliente.razao_social',
        read_only=True
    )
    representante_nome = serializers.SerializerMethodField()
    mes_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Meta
        fields = [
            'id', 'cliente', 'cliente_razao_social',
            'representante_nome',
            'mes', 'mes_nome', 'ano', 'valor', 'dias_uteis'
        ]
        read_only_fields = ['id']
    
    def get_mes_nome(self, obj):
        import calendar
        return calendar.month_name[obj.mes].capitalize()
    
    def get_representante_nome(self, obj):
        if obj.cliente and obj.cliente.cadastrado_por:
            return obj.cliente.cadastrado_por.get_full_name() or obj.cliente.cadastrado_por.username
        return None


# ===== TAREFAS =====

class AcaoTarefaSerializer(serializers.ModelSerializer):
    """Serializer para ações/comentários de tarefas"""
    registrado_por_nome = serializers.CharField(
        source='registrado_por.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = AcaoTarefa
        fields = [
            'id', 'tarefa', 'descricao', 'arquivo',
            'data_registro', 'registrado_por', 'registrado_por_nome'
        ]
        read_only_fields = ['id', 'data_registro']


class TarefaSerializer(serializers.ModelSerializer):
    """Serializer para tarefas (Kanban)"""
    criado_por_nome = serializers.CharField(
        source='criado_por.get_full_name',
        read_only=True
    )
    iniciado_por_nome = serializers.CharField(
        source='iniciado_por.get_full_name',
        read_only=True,
        allow_null=True
    )
    finalizado_por_nome = serializers.CharField(
        source='finalizado_por.get_full_name',
        read_only=True,
        allow_null=True
    )
    acoes = AcaoTarefaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tarefa
        fields = [
            'id', 'titulo', 'descricao', 'status', 'prioridade',
            'data_criacao', 'criado_por', 'criado_por_nome',
            'data_inicio', 'iniciado_por', 'iniciado_por_nome',
            'data_finalizacao', 'finalizado_por', 'finalizado_por_nome',
            'acoes'
        ]
        read_only_fields = [
            'id', 'data_criacao', 'criado_por',
            'data_inicio', 'iniciado_por',
            'data_finalizacao', 'finalizado_por'
        ]


# ===== PROSPECÇÃO =====

class AcaoProspeccaoSerializer(serializers.ModelSerializer):
    """Serializer para ações de prospecção"""
    registrado_por_nome = serializers.CharField(
        source='registrado_por.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = AcaoProspeccao
        fields = [
            'id', 'prospeccao', 'descricao', 'arquivo',
            'data_registro', 'registrado_por', 'registrado_por_nome'
        ]
        read_only_fields = ['id', 'data_registro']


class ProspeccaoSerializer(serializers.ModelSerializer):
    """Serializer para prospecções (Funil de Vendas)"""
    cliente_razao_social = serializers.CharField(
        source='cliente.razao_social',
        read_only=True
    )
    criado_por_nome = serializers.CharField(
        source='criado_por.get_full_name',
        read_only=True
    )
    iniciado_por_nome = serializers.CharField(
        source='iniciado_por.get_full_name',
        read_only=True,
        allow_null=True
    )
    finalizado_por_nome = serializers.CharField(
        source='finalizado_por.get_full_name',
        read_only=True,
        allow_null=True
    )
    acoes = AcaoProspeccaoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Prospeccao
        fields = [
            'id', 'cliente', 'cliente_razao_social',
            'tipo_servico', 'duracao_meses', 'viagens_aproximadas',
            'valor_medio_viagem', 'valor_total',
            'status', 'data_criacao', 'criado_por', 'criado_por_nome',
            'data_inicio_negociacao', 'iniciado_por', 'iniciado_por_nome',
            'data_finalizacao', 'finalizado_por', 'finalizado_por_nome',
            'acoes'
        ]
        read_only_fields = [
            'id', 'data_criacao', 'criado_por',
            'data_inicio_negociacao', 'iniciado_por',
            'data_finalizacao', 'finalizado_por'
        ]


# ===== DASHBOARD / RELATÓRIOS =====

class DashboardMensalSerializer(serializers.Serializer):
    """Serializer para dados do dashboard mensal"""
    mes = serializers.IntegerField()
    ano = serializers.IntegerField()
    faturamento_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    quantidade_servicos = serializers.IntegerField()
    meta_valor = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    percentual_meta = serializers.FloatField(allow_null=True)
    dias_restantes = serializers.IntegerField()


class ClienteRankingSerializer(serializers.Serializer):
    """Serializer para ranking de clientes"""
    cliente_id = serializers.IntegerField()
    razao_social = serializers.CharField()
    total_viagens = serializers.IntegerField()
    faturamento_total = serializers.DecimalField(max_digits=15, decimal_places=2)
