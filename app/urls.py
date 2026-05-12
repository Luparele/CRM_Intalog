from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # URL da Home (página principal que carrega a estrutura)
    path('', views.home_page, name='home'),

    # --- URLs PARA OS BLOCOS DO DASHBOARD (HTMX) ---
    path('dash/mensal/', views.get_dashboard_mensal, name='get-dash-mensal'),
    path('dash/trimestral/', views.get_dashboard_trimestral, name='get-dash-trimestral'),
    path('dash/anual/', views.get_dashboard_anual, name='get-dash-anual'),
    path('dash/top-clientes/', views.get_dashboard_top_clientes, name='get-dash-top-clientes'),
    
    # URLs para gerenciamento de Representantes (Usuários)
    path('representantes/', views.RepresentanteListView.as_view(), name='representante-list'),
    path('representantes/novo/', views.RepresentanteCreateView.as_view(), name='representante-create'),
    path('representantes/<int:pk>/editar/', views.RepresentanteUpdateView.as_view(), name='representante-update'),
    path('representantes/<int:pk>/detalhe/', views.detalhe_representante, name='detalhe-representante'),

    # URLs para gerenciamento de Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/deletar/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
    
    # URLs de Promoção de Prospect (HTMX)
    path('clientes/promover/<int:pk>/', views.promover_prospect_modal, name='promover-prospect-modal'),
    path('clientes/promover/<int:pk>/salvar/', views.salvar_promocao_prospect, name='salvar-promocao-prospect'),

    # URLs para gerenciamento de Serviços (Transportes)
    path('servicos/', views.ServicoListView.as_view(), name='servico-list'),
    path('servicos/novo/', views.ServicoCreateView.as_view(), name='servico-create'),
    path('servicos/<int:pk>/editar/', views.ServicoUpdateView.as_view(), name='servico-update'),
    path('servicos/<int:pk>/editar-modal/', views.ServicoUpdateView.as_view(), name='servico-update-modal'),
    path('servicos/<int:pk>/deletar/', views.ServicoDeleteView.as_view(), name='servico-delete'),
    path('servicos/historico/<int:cliente_id>/<int:mes>/<int:ano>/', views.servico_historico_modal, name='servico-historico-modal'),
    
    # URLs de API
    path('ajax/add-tipo-servico/', views.add_tipo_servico_ajax, name='add-tipo-servico'),
    # --- NOVA LINHA ADICIONADA ABAIXO ---
    path('ajax/consulta-cnpj/<str:cnpj>/', views.consulta_cnpj_api, name='consulta-cnpj-api'),

    # URLs para Metas
    path('metas/', views.MetaListView.as_view(), name='meta-list'),
    path('metas/nova/', views.MetaCreateView.as_view(), name='meta-create'),
    path('metas/<int:pk>/editar/', views.MetaUpdateView.as_view(), name='meta-update'),
    path('metas/<int:pk>/deletar/', views.MetaDeleteView.as_view(), name='meta-delete'),


    # URLs para Agenda / Tarefas
    path('agenda/', views.agenda_view, name='agenda'),
    path('tarefas/', views.tarefas_view, name='tarefas'), # NOVA PAGINA
    path('tarefas/check-alert/', views.check_tarefas_pendentes, name='check_tarefas_alert'),
    path('tarefas/marcar-visualizada/<int:pk>/', views.marcar_visualizada, name='marcar-visualizada'),
    path('tarefas/marcar-todas-visualizadas/', views.marcar_todas_visualizadas, name='marcar_todas_visualizadas'),
    path('tarefas/<int:pk>/concluir/<str:status>/', views.concluir_tarefa, name='concluir-tarefa'),
    path('tarefas/criar/', views.criar_tarefa_agendada, name='criar-tarefa-agendada'), # Nova rota
    path('tarefas/<int:pk>/detalhe/', views.detalhe_tarefa_agendada, name='detalhe-tarefa-agendada'),
    path('agenda/carregar-mais/', views.carregar_mais_tarefas, name='carregar-mais-tarefas'),
    path('tarefa/criar/', views.criar_tarefa, name='criar-tarefa'),
    path('tarefa/<int:pk>/detalhe/', views.detalhe_tarefa, name='detalhe-tarefa'),
    path('tarefa/<int:pk>/gravar-acao/', views.gravar_acao, name='gravar-acao'),
    path('tarefa/<int:pk>/iniciar/', views.iniciar_tarefa, name='iniciar-tarefa'),
    path('tarefa/<int:pk>/finalizar/', views.finalizar_tarefa, name='finalizar-tarefa'),

    # URLs para Prospecção (Funil)
    path('prospeccao/', views.prospeccao_view, name='prospeccao'),
    path('prospeccao/dashboard-content/', views.dashboard_prospeccao, name='dashboard-prospeccao'),
    path('prospeccao/nova/', views.criar_prospeccao, name='criar-prospeccao'),
    path('prospeccao/<int:pk>/detalhe/', views.detalhe_prospeccao, name='detalhe-prospeccao'),
    path('prospeccao/<int:pk>/iniciar/', views.iniciar_prospeccao, name='iniciar-prospeccao'),
    path('prospeccao/<int:pk>/editar/', views.editar_prospeccao, name='editar-prospeccao'),
    path('prospeccao/<int:pk>/gravar_acao/', views.gravar_acao_prospeccao, name='gravar-acao-prospeccao'),
    path('prospeccao/<int:pk>/finalizar/', views.finalizar_prospeccao, name='finalizar-prospeccao'),
    path('prospeccao/novo-cliente/', views.criar_cliente_prospeccao_modal, name='criar-cliente-prospeccao-modal'),
    path('prospeccao/salvar-cliente/', views.salvar_cliente_prospeccao, name='salvar-cliente-prospeccao'),

    # URLs de Relatórios
    path('relatorios/', views.relatorio_page, name='relatorio-page'),
    path('relatorios/exportar/', views.exportar_relatorio, name='exportar-relatorio'),
    path('api/cliente-search/', views.cliente_search_api, name='cliente-search-api'),

    # URL de Direitos
    path('direitos/', views.direitos_page, name='direitos'),
    
    # URLs para Gestão de Feriados
    path('feriados/', views.gerenciar_feriados_modal, name='gerenciar-feriados'),
    path('feriados/adicionar/', views.adicionar_feriado, name='adicionar-feriado'),
    path('feriados/deletar/<int:pk>/', views.deletar_feriado, name='deletar-feriado'),

    # URL de Documentação da API
    path('api-docs/', views.api_documentation, name='api-documentation'),

    # URL para Backup Manual (Superuser)
    path('backup/manual/', views.manual_backup, name='manual-backup'),

    # URL para servir arquivos do Google Drive (Mídia)
    path('media-drive/<path:path>', views.serve_drive_file, name='serve-drive-file'),
]