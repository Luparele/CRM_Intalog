from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token

from app.models import Cliente, TipoServico, Servico, Profile
from app.api_views import INTEGRACAO_GROUP_NAME


class Command(BaseCommand):
    help = (
        "Cria ou atualiza o usuário 'integracao-globus' com permissões restritas "
        "(ver/criar/editar serviços e consultar clientes/tipos de serviço, sem excluir e sem admin) "
        "e gera/exibe seu Token da API."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='integracao-globus',
            help="Nome do usuário de integração (padrão: integracao-globus).",
        )
        parser.add_argument(
            '--regenerar',
            action='store_true',
            help="Apaga o token atual e gera um novo token aleatório (útil em caso de vazamento).",
        )
        parser.add_argument(
            '--token',
            type=str,
            default=None,
            help="Define manualmente uma chave de token específica (ex: para sincronizar o mesmo token no PythonAnywhere).",
        )

    def handle(self, *args, **options):
        username = options['username']
        regenerar = options['regenerar']
        custom_token = options['token']

        if custom_token and regenerar:
            raise CommandError("Não use --regenerar e --token ao mesmo tempo.")

        if custom_token and len(custom_token.strip()) < 20:
            raise CommandError("O token informado em --token deve ter pelo menos 20 caracteres.")

        # 1. Configurar Grupo de Permissões Restritas
        group, _ = Group.objects.get_or_create(name=INTEGRACAO_GROUP_NAME)

        ct_servico = ContentType.objects.get_for_model(Servico)
        ct_cliente = ContentType.objects.get_for_model(Cliente)
        ct_tipo = ContentType.objects.get_for_model(TipoServico)

        allowed_perms = [
            Permission.objects.get(content_type=ct_servico, codename='view_servico'),
            Permission.objects.get(content_type=ct_servico, codename='add_servico'),
            Permission.objects.get(content_type=ct_servico, codename='change_servico'),
            Permission.objects.get(content_type=ct_cliente, codename='view_cliente'),
            Permission.objects.get(content_type=ct_tipo, codename='view_tiposervico'),
        ]
        group.permissions.set(allowed_perms)

        # 2. Criar ou atualizar usuário sem senha web e sem privilégios administrativos
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': 'Integração',
                'last_name': 'Globus',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
            },
        )
        user.first_name = 'Integração'
        user.last_name = 'Globus'
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_unusable_password()
        user.save()

        user.groups.set([group])
        user.user_permissions.clear()

        # 3. Ajustar Profile (não representante, não admin/comercial)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.setor = 'GERENTE'
        profile.eh_representante = False
        profile.status = 'ATIVO'
        profile.save()

        # 4. Gerenciar Token
        if regenerar:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            token_action = "REGENERADO"
        elif custom_token:
            custom_token = custom_token.strip()
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user, key=custom_token)
            token_action = "DEFINIDO MANUALMENTE"
        else:
            token, token_created = Token.objects.get_or_create(user=user)
            token_action = "CRIADO" if token_created else "MANTIDO"

        self.stdout.write(self.style.SUCCESS(f"Usuário '{user.username}' {'criado' if created else 'atualizado'} com sucesso!"))
        self.stdout.write(f"Nome exibido nos lançamentos: {user.get_full_name()}")
        self.stdout.write(f"Login Web / Admin: BLOQUEADO (senha inutilizável, is_staff=False, is_superuser=False)")
        self.stdout.write(f"Grupo: {group.name}")
        self.stdout.write("Permissões ativas:")
        for p in allowed_perms:
            self.stdout.write(f"  - {p.content_type.app_label}.{p.codename}")
        self.stdout.write(self.style.WARNING("Permissão de exclusão (delete_servico): NEGADA"))
        self.stdout.write(self.style.SUCCESS(f"\nToken ({token_action}): {token.key}"))
