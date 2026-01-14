from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Profile, Cliente, ClienteProspect, Servico, TipoServico, Meta, 
    Tarefa, AcaoTarefa, Prospeccao, AcaoProspeccao
)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fk_name = 'user'

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_eh_representante')
    list_select_related = ('profile', )

    def get_eh_representante(self, instance):
        return instance.profile.eh_representante
    get_eh_representante.short_description = 'Representante'
    get_eh_representante.boolean = True

@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # --- ALTERAÇÃO: Removido 'filial' do list_display e list_filter ---
    list_display = ('razao_social', 'cnpj', 'nome_contato', 'cadastrado_por')
    search_fields = ('razao_social', 'cnpj')
    list_filter = ('cadastrado_por',)

@admin.register(ClienteProspect)
class ClienteProspectAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'nome_contato', 'email_contato', 'cadastrado_por')
    search_fields = ('razao_social', 'cnpj', 'nome_contato')
    list_filter = ('cadastrado_por', 'data_cadastro')

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo_servico', 'data_servico', 'valor', 'fechado_por')
    search_fields = ('cliente__razao_social',)
    list_filter = ('data_servico', 'fechado_por', 'tipo_servico')

@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'get_representante', 'mes', 'ano', 'valor', 'dias_uteis')
    list_filter = ('ano', 'mes', 'cliente__cadastrado_por') 
    search_fields = ('cliente__razao_social', 'cliente__cadastrado_por__username')
    
    def get_representante(self, obj):
        return obj.cliente.cadastrado_por.get_full_name() or obj.cliente.cadastrado_por.username
    get_representante.short_description = 'Representante'
    get_representante.admin_order_field = 'cliente__cadastrado_por'

class AcaoTarefaInline(admin.TabularInline):
    model = AcaoTarefa
    extra = 1
    readonly_fields = ('registrado_por', 'data_registro')
    fields = ('descricao', 'arquivo', 'registrado_por', 'data_registro')

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'criado_por', 'data_criacao', 'iniciado_por', 'finalizado_por')
    list_filter = ('status', 'criado_por', 'iniciado_por', 'finalizado_por')
    search_fields = ('titulo', 'descricao')
    readonly_fields = ('data_criacao', 'data_inicio', 'data_finalizacao')
    inlines = [AcaoTarefaInline]
    fieldsets = (
        (None, {'fields': ('titulo', 'descricao', 'status')}),
        ('Histórico', {
            'classes': ('collapse',),
            'fields': ('criado_por', 'data_criacao', 'iniciado_por', 'data_inicio', 'finalizado_por', 'data_finalizacao'),
        }),
    )

@admin.register(AcaoTarefa)
class AcaoTarefaAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'registrado_por', 'data_registro')
    list_filter = ('registrado_por', 'data_registro')
    search_fields = ('descricao', 'tarefa__titulo')

class AcaoProspeccaoInline(admin.TabularInline):
    model = AcaoProspeccao
    extra = 0 
    readonly_fields = ('descricao', 'registrado_por', 'data_registro')
    fields = ('descricao', 'arquivo', 'registrado_por', 'data_registro')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Prospeccao)
class ProspeccaoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'status', 'valor_total', 'criado_por', 'data_criacao', 'finalizado_por')
    list_filter = ('status', 'tipo_servico', 'criado_por', 'finalizado_por')
    search_fields = ('cliente__razao_social',)
    readonly_fields = ('data_criacao', 'data_inicio_negociacao', 'data_finalizacao')
    inlines = [AcaoProspeccaoInline]
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('cliente', 'status', 'tipo_servico', 'valor_total')
        }),
        ('Estimativas', {
            'fields': ('duracao_meses', 'viagens_aproximadas', 'valor_medio_viagem')
        }),
        ('Histórico', {
            'classes': ('collapse',),
            'fields': ('criado_por', 'data_criacao', 'iniciado_por', 'data_inicio_negociacao', 'finalizado_por', 'data_finalizacao'),
        }),
    )

@admin.register(AcaoProspeccao)
class AcaoProspeccaoAdmin(admin.ModelAdmin):
    list_display = ('prospeccao', 'registrado_por', 'data_registro')
    list_filter = ('registrado_por', 'data_registro')
    search_fields = ('descricao', 'prospeccao__cliente__razao_social')