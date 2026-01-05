from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import date
import calendar

from .models import Cliente, Servico, Meta
from .serializers import (
    UserSerializer, ClienteSerializer, ServicoSerializer,
    ServicoCreateSerializer, DashboardMensalSerializer
)
from django.contrib.auth.models import User


class IsGestaoOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.profile.tem_acesso_gestao
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsGestaoOrReadOnly]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().select_related('cadastrado_por')
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.profile.is_representante:
            return queryset.filter(cadastrado_por=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(cadastrado_por=self.request.user)


class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all().select_related('cliente', 'tipo_servico')
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ServicoCreateSerializer
        return ServicoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.profile.is_representante:
            queryset = queryset.filter(cliente__cadastrado_por=self.request.user)
        
        ano = self.request.query_params.get('ano')
        mes = self.request.query_params.get('mes')
        if ano:
            queryset = queryset.filter(data_servico__year=ano)
        if mes:
            queryset = queryset.filter(data_servico__month=mes)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(fechado_por=self.request.user)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
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
