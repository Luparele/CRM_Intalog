from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    UserViewSet,
    ClienteViewSet,
    ServicoViewSet,
    DashboardViewSet,
)

# Router para endpoints RESTful
router = DefaultRouter()

# Registrar ViewSets
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'servicos', ServicoViewSet, basename='servico')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# URLs da API
urlpatterns = [
    # Endpoints da API
    path('', include(router.urls)),
]
