from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from app.models import Cliente, TipoServico, Servico


class IntegracaoGlobusAPITests(TestCase):
    def setUp(self):
        call_command('configurar_integracao_globus')
        self.integracao_user = User.objects.get(username='integracao-globus')
        self.token = Token.objects.get(user=self.integracao_user)

        self.rep = User.objects.create_user(username='rep_teste', password='123', first_name='Carlos')
        self.rep.profile.setor = 'REPRESENTANTE'
        self.rep.profile.eh_representante = True
        self.rep.profile.save()

        self.tipo = TipoServico.objects.create(nome='DEDICADO')
        self.cliente = Cliente.objects.create(
            cnpj='12.345.678/0001-90',
            razao_social='Transportadora Exemplo LTDA',
            endereco='Rua A, 100',
            nome_contato='Maria',
            telefone_contato='11999999999',
            cadastrado_por=self.rep,
        )

        self.client_api = APIClient()
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_sem_token_retorna_401(self):
        anon = APIClient()
        resp = anon.get('/api/servicos/')
        self.assertEqual(resp.status_code, 401)

    def test_usuario_integracao_nao_tem_senha_web_nem_admin(self):
        self.assertFalse(self.integracao_user.has_usable_password())
        self.assertFalse(self.integracao_user.is_staff)
        self.assertFalse(self.integracao_user.is_superuser)

    def test_leitura_clientes_e_tipos_servico_com_busca_cnpj(self):
        resp_tipos = self.client_api.get('/api/tipos-servico/')
        self.assertEqual(resp_tipos.status_code, 200)
        self.assertEqual(resp_tipos.data['count'], 1)

        # Busca por CNPJ sem pontuação encontra CNPJ com pontuação
        resp_cli = self.client_api.get('/api/clientes/?cnpj=12345678000190')
        self.assertEqual(resp_cli.status_code, 200)
        self.assertEqual(resp_cli.data['count'], 1)
        self.assertEqual(resp_cli.data['results'][0]['id'], self.cliente.id)

        # Busca textual por razão social
        resp_search = self.client_api.get('/api/clientes/?search=Transportadora')
        self.assertEqual(resp_search.status_code, 200)
        self.assertEqual(resp_search.data['count'], 1)

    def test_bloqueia_escrita_clientes_e_acesso_usuarios_dashboard(self):
        self.assertEqual(self.client_api.post('/api/clientes/', {
            'cnpj': '99999999000199',
            'razao_social': 'Teste',
            'endereco': 'Rua B',
            'nome_contato': 'João',
            'telefone_contato': '11888888888',
        }).status_code, 403)
        self.assertEqual(self.client_api.delete(f'/api/clientes/{self.cliente.id}/').status_code, 403)
        self.assertEqual(self.client_api.get('/api/usuarios/').status_code, 403)
        self.assertEqual(self.client_api.get('/api/dashboard/mensal/').status_code, 403)

    def test_fluxo_completo_servicos_ver_criar_editar_e_bloquear_exclusao(self):
        # 1. Criar serviço
        resp_create = self.client_api.post('/api/servicos/', {
            'cliente': self.cliente.id,
            'tipo_servico': self.tipo.id,
            'data_servico': '2026-11-25',
            'quantidade': 3,
            'valor': '4500.50',
        }, format='json')
        self.assertEqual(resp_create.status_code, 201)
        servico_id = resp_create.data['id']
        self.assertEqual(resp_create.data['fechado_por'], self.integracao_user.id)
        self.assertEqual(resp_create.data['fechado_por_nome'], 'Integração Globus')

        # 2. Listar / Filtrar serviço (inclusive de cliente pertencente a outro representante)
        resp_list = self.client_api.get(f'/api/servicos/?cliente={self.cliente.id}&data_servico=2026-11-25')
        self.assertEqual(resp_list.status_code, 200)
        self.assertEqual(resp_list.data['count'], 1)

        # 3. Editar serviço (PATCH)
        resp_patch = self.client_api.patch(f'/api/servicos/{servico_id}/', {
            'quantidade': 4,
            'valor': '6000.00',
        }, format='json')
        self.assertEqual(resp_patch.status_code, 200)
        self.assertEqual(Decimal(resp_patch.data['valor']), Decimal('6000.00'))

        # 4. Tentar excluir serviço -> DEVE retornar 403 Forbidden
        resp_delete = self.client_api.delete(f'/api/servicos/{servico_id}/')
        self.assertEqual(resp_delete.status_code, 403)
        self.assertTrue(Servico.objects.filter(id=servico_id).exists())

    def test_regenerar_token_invalida_anterior(self):
        old_key = self.token.key
        call_command('configurar_integracao_globus', regenerar=True)
        new_key = Token.objects.get(user=self.integracao_user).key
        self.assertNotEqual(old_key, new_key)

        # Token antigo bloqueado
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Token {old_key}')
        self.assertEqual(self.client_api.get('/api/servicos/').status_code, 401)

        # Token novo liberado
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Token {new_key}')
        self.assertEqual(self.client_api.get('/api/servicos/').status_code, 200)
