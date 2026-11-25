import re
from datetime import date
import calendar

from django.contrib.auth.models import User
from django.db.models import Sum, F, Value
from django.db.models.functions import Replace
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cliente, TipoServico, Servico, Meta
from .serializers import (
    UserSerializer,
    ClienteSerializer,
    TipoServicoSerializer,
    ServicoSerializer,
    DashboardMensalSerializer,
)

INTEGRACAO_GROUP_NAME = 'Integracao API'


def is_integracao_user(user):
    return bool(
        user
        and user.is_authenticated
        and user.groups.filter(name=INTEGRACAO_GROUP_NAME).exists()
    )


def is_active_crm_user(user):
    if not user or not user.is_authenticated or not user.is_active:
        return False
    profile = getattr(user, 'profile', None)
    if profile and profile.status == 'INATIVO':
        return False
    return True


def clean_cnpj(value):
    return re.sub(r'\D', '', value or '')


class StrictDjangoModelPermissions(permissions.DjangoModelPermissions):
    """Exige também permissão view_<model> para métodos de leitura (GET/HEAD/OPTIONS)."""
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsGestaoOrReadOnlyNonIntegracao(permissions.BasePermission):
    """Bloqueia usuários de integração e restringe escrita à gestão/staff."""
    def has_permission(self, request, view):
        user = request.user
        if not is_active_crm_user(user) or is_integracao_user(user):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        profile = getattr(user, 'profile', None)
        return bool(user.is_staff or (profile and profile.tem_acesso_gestao))


class ClienteAPIPermission(permissions.BasePermission):
    """
    - Usuário de integração: segue estritamente DjangoModelPermissions (somente GET se tiver view_cliente).
    - Usuários internos do CRM: leitura conforme perfil; criação/edição para gestão/staff/representante; exclusão só gestão/staff.
    """
    def has_permission(self, request, view):
        user = request.user
        if not is_active_crm_user(user):
            return False
        if is_integracao_user(user):
            return StrictDjangoModelPermissions().has_permission(request, view)

        profile = getattr(user, 'profile', None)
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return bool(user.is_staff or (profile and profile.tem_acesso_gestao))
        return bool(
            user.is_staff
            or (profile and (profile.tem_acesso_gestao or profile.is_representante))
        )


class TipoServicoAPIPermission(permissions.BasePermission):
    """Somente leitura (GET/HEAD/OPTIONS) para usuários ativos e integrações autorizadas."""
    def has_permission(self, request, view):
        user = request.user
        if not is_active_crm_user(user):
            return False
        if request.method not in permissions.SAFE_METHODS:
            return False
        if is_integracao_user(user):
            return StrictDjangoModelPermissions().has_permission(request, view)
        return True


class ServicoAPIPermission(permissions.BasePermission):
    """
    - Usuário de integração: segue estritamente DjangoModelPermissions
      (view_servico, add_servico, change_servico -> GET, POST, PUT, PATCH; sem delete_servico -> DELETE bloqueado com 403).
    - Usuários internos do CRM: leitura para perfis autorizados; criação/edição/exclusão apenas para gestão/staff.
    """
    def has_permission(self, request, view):
        user = request.user
        if not is_active_crm_user(user):
            return False
        if is_integracao_user(user):
            return StrictDjangoModelPermissions().has_permission(request, view)

        profile = getattr(user, 'profile', None)
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(user.is_staff or (profile and profile.tem_acesso_gestao))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile').order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsGestaoOrReadOnlyNonIntegracao]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().select_related('cadastrado_por').order_by('razao_social', 'id')
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated, ClienteAPIPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['razao_social', 'cnpj', 'nome_contato']

    def get_queryset(self):
        queryset = super().get_queryset()
        profile = getattr(self.request.user, 'profile', None)
        if profile and profile.is_representante and not is_integracao_user(self.request.user):
            queryset = queryset.filter(cadastrado_por=self.request.user)

        cnpj_param = self.request.query_params.get('cnpj')
        if cnpj_param:
            digits = clean_cnpj(cnpj_param)
            if digits:
                queryset = queryset.annotate(
                    cnpj_limpo=Replace(
                        Replace(
                            Replace(
                                Replace(F('cnpj'), Value('.'), Value('')),
                                Value('/'), Value('')
                            ),
                            Value('-'), Value('')
                        ),
                        Value(' '), Value('')
                    )
                ).filter(cnpj_limpo=digits)

        return queryset

    def perform_create(self, serializer):
        serializer.save(cadastrado_por=self.request.user)


class TipoServicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoServico.objects.all().order_by('nome')
    serializer_class = TipoServicoSerializer
    permission_classes = [permissions.IsAuthenticated, TipoServicoAPIPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']


class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all().select_related(
        'cliente', 'tipo_servico', 'fechado_por'
    ).order_by('-data_servico', '-id')
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated, ServicoAPIPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        profile = getattr(self.request.user, 'profile', None)
        if profile and profile.is_representante and not is_integracao_user(self.request.user):
            queryset = queryset.filter(cliente__cadastrado_por=self.request.user)

        params = self.request.query_params

        cliente_id = params.get('cliente')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)

        cnpj_param = params.get('cnpj')
        if cnpj_param:
            digits = clean_cnpj(cnpj_param)
            if digits:
                queryset = queryset.annotate(
                    cliente_cnpj_limpo=Replace(
                        Replace(
                            Replace(
                                Replace(F('cliente__cnpj'), Value('.'), Value('')),
                                Value('/'), Value('')
                            ),
                            Value('-'), Value('')
                        ),
                        Value(' '), Value('')
                    )
                ).filter(cliente_cnpj_limpo=digits)

        tipo_servico_id = params.get('tipo_servico')
        if tipo_servico_id:
            queryset = queryset.filter(tipo_servico_id=tipo_servico_id)

        data_servico = params.get('data_servico')
        if data_servico:
            queryset = queryset.filter(data_servico=data_servico)

        data_inicio = params.get('data_inicio')
        if data_inicio:
            queryset = queryset.filter(data_servico__gte=data_inicio)

        data_fim = params.get('data_fim')
        if data_fim:
            queryset = queryset.filter(data_servico__lte=data_fim)

        ano = params.get('ano')
        if ano:
            queryset = queryset.filter(data_servico__year=ano)

        mes = params.get('mes')
        if mes:
            queryset = queryset.filter(data_servico__month=mes)

        fechado_por_username = params.get('fechado_por_username')
        if fechado_por_username:
            queryset = queryset.filter(fechado_por__username=fechado_por_username)

        return queryset

    def perform_create(self, serializer):
        serializer.save(fechado_por=self.request.user)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsGestaoOrReadOnlyNonIntegracao]

    @action(detail=False, methods=['get'])
    def mensal(self, request):
        hoje = date.today()
        mes = int(request.query_params.get('mes', hoje.month))
        ano = int(request.query_params.get('ano', hoje.year))

        base_qs = Servico.objects.filter(data_servico__year=ano, data_servico__month=mes)

        if request.user.profile.is_representante:
            base_qs = base_qs.filter(cliente__cadastrado_por=request.user)

        fat_total = base_qs.aggregate(s=Sum('valor'))['s'] or 0
        qtd_total = base_qs.aggregate(c=Sum('quantidade'))['c'] or 0

        # Meta agora é por cliente - soma as metas dos clientes
        if request.user.profile.is_representante:
            val_meta = Meta.objects.filter(
                cliente__cadastrado_por=request.user,
                mes=mes,
                ano=ano
            ).aggregate(s=Sum('valor'))['s'] or 0
        else:
            val_meta = Meta.objects.filter(mes=mes, ano=ano).aggregate(s=Sum('valor'))['s'] or 0

        percentual = (fat_total / val_meta * 100) if val_meta > 0 else None

        _, last_day = calendar.monthrange(ano, mes)
        from django.utils import timezone
        now = timezone.now().date()

        if ano < now.year or (ano == now.year and mes < now.month):
            dias_rest = 0
        elif ano == now.year and mes == now.month:
            dias_rest = max(0, last_day - now.day)
        else:
            dias_rest = last_day

        data = {
            'mes': mes,
            'ano': ano,
            'faturamento_total': fat_total,
            'quantidade_servicos': qtd_total,
            'meta_valor': val_meta if val_meta > 0 else None,
            'percentual_meta': percentual,
            'dias_restantes': dias_rest
        }

        serializer = DashboardMensalSerializer(data)
        return Response(serializer.data)
