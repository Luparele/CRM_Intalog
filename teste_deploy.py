"""
===============================================================================
SCRIPT DE TESTE GERAL - CRM INTALOG (Zenith CRM)
Verifica todas as funcionalidades antes do deploy
Execute: python teste_deploy.py
===============================================================================
"""
import os
import sys
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM_Comercial.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client
from django.urls import reverse, NoReverseMatch
from decimal import Decimal
from datetime import date, timedelta
import traceback

# Cores para output
class Colors:
    OK = '\033[92m'      # Verde
    FAIL = '\033[91m'    # Vermelho
    WARN = '\033[93m'    # Amarelo
    INFO = '\033[94m'    # Azul
    END = '\033[0m'      # Reset

def ok(msg):
    print(f"{Colors.OK}✓ {msg}{Colors.END}")

def fail(msg):
    print(f"{Colors.FAIL}✗ {msg}{Colors.END}")

def warn(msg):
    print(f"{Colors.WARN}⚠ {msg}{Colors.END}")

def info(msg):
    print(f"{Colors.INFO}ℹ {msg}{Colors.END}")

def header(msg):
    print(f"\n{Colors.INFO}{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}{Colors.END}")

# Contadores
testes_ok = 0
testes_fail = 0
testes_warn = 0

def test(descricao, funcao):
    global testes_ok, testes_fail
    try:
        resultado = funcao()
        if resultado:
            ok(descricao)
            testes_ok += 1
            return True
        else:
            fail(descricao)
            testes_fail += 1
            return False
    except Exception as e:
        fail(f"{descricao} - ERRO: {str(e)}")
        testes_fail += 1
        return False

# ============================================================================
# TESTES DE BANCO DE DADOS
# ============================================================================
def teste_conexao_banco():
    """Testa conexão com o banco de dados"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        return cursor.fetchone()[0] == 1

def teste_tabelas_existem():
    """Verifica se todas as tabelas necessárias existem"""
    tabelas_necessarias = [
        'app_profile',
        'app_cliente',
        'app_clienteprospect', 
        'app_servico',
        'app_tiposervico',
        'app_meta',
        'app_tarefa',
        'app_acaotarefa',
        'app_prospeccao',
        'app_acaoprospeccao',
        'auth_user',
    ]
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas_existentes = [row[0] for row in cursor.fetchall()]
    
    for tabela in tabelas_necessarias:
        if tabela not in tabelas_existentes:
            print(f"    Tabela faltando: {tabela}")
            return False
    return True

def teste_estrutura_meta():
    """Verifica se a tabela Meta tem a estrutura correta (cliente em vez de representante)"""
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(app_meta);")
        colunas = [row[1] for row in cursor.fetchall()]
    
    if 'cliente_id' not in colunas:
        print(f"    Coluna cliente_id não encontrada. Colunas: {colunas}")
        return False
    if 'representante_id' in colunas:
        print(f"    Coluna representante_id ainda existe (deveria ter sido removida)")
        return False
    return True

# ============================================================================
# TESTES DE MODELS
# ============================================================================
def teste_importar_models():
    """Testa importação de todos os models"""
    from app.models import (
        Profile, Cliente, ClienteProspect, Servico, TipoServico,
        Meta, Tarefa, AcaoTarefa, Prospeccao, AcaoProspeccao
    )
    return True

def teste_criar_cliente():
    """Testa criação de cliente"""
    from app.models import Cliente
    user = User.objects.first()
    if not user:
        print("    Nenhum usuário encontrado para teste")
        return False
    
    cliente = Cliente.objects.create(
        cnpj='12345678000199',
        razao_social='CLIENTE TESTE DEPLOY',
        endereco='Rua Teste, 123',
        nome_contato='Contato Teste',
        telefone_contato='11999999999',
        cadastrado_por=user
    )
    cliente_id = cliente.id
    cliente.delete()
    return cliente_id is not None

def teste_criar_meta_por_cliente():
    """Testa criação de meta vinculada a cliente (nova estrutura)"""
    from app.models import Cliente, Meta
    user = User.objects.first()
    if not user:
        return False
    
    # Cria cliente temporário
    cliente = Cliente.objects.create(
        cnpj='98765432000188',
        razao_social='CLIENTE META TESTE',
        cadastrado_por=user
    )
    
    # Cria meta vinculada ao cliente
    meta = Meta.objects.create(
        cliente=cliente,
        mes=1,
        ano=2026,
        dias_uteis=22,
        valor=Decimal('50000.00')
    )
    
    # Verifica se consegue acessar o representante via cliente
    rep_nome = meta.cliente.cadastrado_por.username
    
    # Limpa
    meta.delete()
    cliente.delete()
    
    return rep_nome is not None

def teste_criar_servico():
    """Testa criação de serviço"""
    from app.models import Cliente, Servico, TipoServico
    user = User.objects.first()
    if not user:
        return False
    
    cliente = Cliente.objects.create(
        cnpj='11111111000111',
        razao_social='CLIENTE SERVICO TESTE',
        cadastrado_por=user
    )
    
    tipo, _ = TipoServico.objects.get_or_create(nome='TESTE')
    
    servico = Servico.objects.create(
        cliente=cliente,
        tipo_servico=tipo,
        data_servico=date.today(),
        quantidade=10,
        valor=Decimal('5000.00'),
        fechado_por=user
    )
    
    servico_id = servico.id
    servico.delete()
    cliente.delete()
    
    return servico_id is not None

# ============================================================================
# TESTES DE VIEWS E URLS
# ============================================================================
def teste_urls_principais():
    """Testa se as URLs principais estão configuradas"""
    urls_para_testar = [
        'app:home',
        'app:cliente-list',
        'app:servico-list',
        'app:meta-list',
        'app:agenda',
        'app:prospeccao',
        'app:relatorios',
        'app:representante-list',
    ]
    
    for url_name in urls_para_testar:
        try:
            reverse(url_name)
        except NoReverseMatch:
            print(f"    URL não encontrada: {url_name}")
            return False
    return True

def teste_acesso_paginas_autenticado():
    """Testa acesso às páginas com usuário autenticado"""
    client = Client()
    user = User.objects.first()
    if not user:
        print("    Nenhum usuário para teste")
        return False
    
    client.force_login(user)
    
    paginas = [
        '/',
        '/clientes/',
        '/servicos/',
        '/metas/',
        '/agenda/',
        '/prospeccao/',
    ]
    
    for pagina in paginas:
        try:
            response = client.get(pagina)
            if response.status_code not in [200, 302]:
                print(f"    Erro na página {pagina}: status {response.status_code}")
                return False
        except Exception as e:
            print(f"    Erro ao acessar {pagina}: {e}")
            return False
    
    return True

def teste_dashboard_mensal():
    """Testa endpoint do dashboard mensal"""
    client = Client()
    user = User.objects.first()
    if not user:
        return False
    
    client.force_login(user)
    response = client.get('/dash/mensal/')
    return response.status_code == 200

def teste_dashboard_trimestral():
    """Testa endpoint do dashboard trimestral"""
    client = Client()
    user = User.objects.first()
    if not user:
        return False
    
    client.force_login(user)
    response = client.get('/dash/trimestral/')
    return response.status_code == 200

def teste_dashboard_anual():
    """Testa endpoint do dashboard anual"""
    client = Client()
    user = User.objects.first()
    if not user:
        return False
    
    client.force_login(user)
    response = client.get('/dash/anual/')
    return response.status_code == 200

# ============================================================================
# TESTES DE FORMS
# ============================================================================
def teste_importar_forms():
    """Testa importação de todos os forms"""
    from app.forms import (
        UserForm, ProfileForm, ServicoForm, MetaForm,
        TarefaForm, ProspeccaoForm, ClienteForm
    )
    return True

def teste_meta_form_usa_cliente():
    """Verifica se MetaForm usa campo cliente (não representante)"""
    from app.forms import MetaForm
    form = MetaForm()
    
    if 'cliente' not in form.fields:
        print("    Campo 'cliente' não encontrado no MetaForm")
        return False
    if 'representante' in form.fields:
        print("    Campo 'representante' ainda existe no MetaForm")
        return False
    return True

# ============================================================================
# TESTES DE SERIALIZERS (API)
# ============================================================================
def teste_importar_serializers():
    """Testa importação dos serializers"""
    from app.serializers import (
        UserSerializer, ClienteSerializer, ServicoSerializer,
        MetaSerializer, TarefaSerializer, ProspeccaoSerializer
    )
    return True

def teste_meta_serializer():
    """Testa se MetaSerializer funciona com cliente"""
    from app.serializers import MetaSerializer
    from app.models import Cliente, Meta
    
    user = User.objects.first()
    if not user:
        return False
    
    cliente = Cliente.objects.create(
        cnpj='22222222000122',
        razao_social='CLIENTE SERIALIZER TESTE',
        cadastrado_por=user
    )
    
    meta = Meta.objects.create(
        cliente=cliente,
        mes=2,
        ano=2026,
        valor=Decimal('30000.00')
    )
    
    serializer = MetaSerializer(meta)
    data = serializer.data
    
    meta.delete()
    cliente.delete()
    
    return 'cliente' in data and 'cliente_razao_social' in data

# ============================================================================
# TESTES DE ADMIN
# ============================================================================
def teste_admin_meta():
    """Testa se admin de Meta está configurado corretamente"""
    from django.contrib import admin
    from app.models import Meta
    
    if Meta not in admin.site._registry:
        print("    Meta não está registrado no admin")
        return False
    
    meta_admin = admin.site._registry[Meta]
    
    # Verifica se list_display não tem 'representante'
    if 'representante' in meta_admin.list_display:
        print("    'representante' ainda está em list_display do MetaAdmin")
        return False
    
    return True

# ============================================================================
# TESTES DE INTEGRIDADE
# ============================================================================
def teste_usuarios_existem():
    """Verifica se há usuários no sistema"""
    count = User.objects.count()
    if count == 0:
        print("    Nenhum usuário encontrado")
        return False
    info(f"    {count} usuário(s) encontrado(s)")
    return True

def teste_profiles_existem():
    """Verifica se todos os usuários têm profile"""
    from app.models import Profile
    users_sem_profile = User.objects.filter(profile__isnull=True).count()
    if users_sem_profile > 0:
        print(f"    {users_sem_profile} usuário(s) sem profile")
        return False
    return True

def teste_representantes_ativos():
    """Lista representantes ativos"""
    from app.models import Profile
    reps = User.objects.filter(profile__setor='REPRESENTANTE', is_active=True)
    info(f"    {reps.count()} representante(s) ativo(s)")
    for rep in reps[:5]:
        info(f"      - {rep.get_full_name() or rep.username}")
    return True

# ============================================================================
# TESTES DE CONFIGURAÇÃO
# ============================================================================
def teste_settings():
    """Verifica configurações importantes"""
    from django.conf import settings
    
    checks = []
    
    # DEBUG deve ser False em produção
    if settings.DEBUG:
        warn("    DEBUG está True (deve ser False em produção)")
    
    # SECRET_KEY não deve ser a padrão
    if 'django-insecure' in settings.SECRET_KEY:
        warn("    SECRET_KEY parece ser a padrão (altere para produção)")
    
    # ALLOWED_HOSTS
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
        warn("    ALLOWED_HOSTS não está configurado adequadamente")
    
    return True

def teste_static_files():
    """Verifica se arquivos estáticos existem"""
    import os
    from django.conf import settings
    
    static_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
    if not os.path.exists(static_dir):
        warn("    Diretório 'staticfiles' não existe. Execute 'collectstatic' antes do deploy")
        return True  # Não é erro crítico
    return True

# ============================================================================
# EXECUÇÃO DOS TESTES
# ============================================================================
def main():
    global testes_ok, testes_fail, testes_warn
    
    print(f"""
{Colors.INFO}╔══════════════════════════════════════════════════════════════╗
║           TESTE GERAL - CRM INTALOG (Zenith CRM)             ║
║                    Verificação de Deploy                      ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")

    # BANCO DE DADOS
    header("BANCO DE DADOS")
    test("Conexão com banco de dados", teste_conexao_banco)
    test("Tabelas necessárias existem", teste_tabelas_existem)
    test("Estrutura da tabela Meta (cliente em vez de representante)", teste_estrutura_meta)
    
    # MODELS
    header("MODELS")
    test("Importação de models", teste_importar_models)
    test("Criação de cliente", teste_criar_cliente)
    test("Criação de meta vinculada a cliente", teste_criar_meta_por_cliente)
    test("Criação de serviço", teste_criar_servico)
    
    # FORMS
    header("FORMS")
    test("Importação de forms", teste_importar_forms)
    test("MetaForm usa campo cliente", teste_meta_form_usa_cliente)
    
    # SERIALIZERS
    header("SERIALIZERS (API)")
    test("Importação de serializers", teste_importar_serializers)
    test("MetaSerializer funciona com cliente", teste_meta_serializer)
    
    # ADMIN
    header("ADMIN")
    test("Configuração do MetaAdmin", teste_admin_meta)
    
    # URLS E VIEWS
    header("URLS E VIEWS")
    test("URLs principais configuradas", teste_urls_principais)
    test("Acesso a páginas autenticado", teste_acesso_paginas_autenticado)
    test("Dashboard mensal", teste_dashboard_mensal)
    test("Dashboard trimestral", teste_dashboard_trimestral)
    test("Dashboard anual", teste_dashboard_anual)
    
    # INTEGRIDADE
    header("INTEGRIDADE DOS DADOS")
    test("Usuários existem", teste_usuarios_existem)
    test("Profiles existem para todos usuários", teste_profiles_existem)
    teste_representantes_ativos()
    
    # CONFIGURAÇÃO
    header("CONFIGURAÇÕES DE DEPLOY")
    test("Verificação de settings", teste_settings)
    test("Arquivos estáticos", teste_static_files)
    
    # RESUMO
    print(f"""
{Colors.INFO}╔══════════════════════════════════════════════════════════════╗
║                        RESUMO DOS TESTES                      ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")
    
    total = testes_ok + testes_fail
    
    print(f"  {Colors.OK}Testes OK:     {testes_ok}{Colors.END}")
    print(f"  {Colors.FAIL}Testes FALHA:  {testes_fail}{Colors.END}")
    print(f"  {Colors.INFO}Total:         {total}{Colors.END}")
    
    if testes_fail == 0:
        print(f"""
{Colors.OK}╔══════════════════════════════════════════════════════════════╗
║  ✓ TODOS OS TESTES PASSARAM! Sistema pronto para deploy.    ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")
        return 0
    else:
        print(f"""
{Colors.FAIL}╔══════════════════════════════════════════════════════════════╗
║  ✗ ALGUNS TESTES FALHARAM! Corrija antes de fazer deploy.   ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")
        return 1

if __name__ == '__main__':
    sys.exit(main())
