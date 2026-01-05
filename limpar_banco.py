"""
Script para limpar banco de dados mantendo usuários e profiles.
Execute: python limpar_banco.py
"""
import os
import sys
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM_Comercial.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection

def limpar_banco():
    """Limpa todas as tabelas exceto auth_user, app_profile e tabelas do sistema Django"""
    
    tabelas_para_limpar = [
        'app_meta',
        'app_acaoprospeccao',
        'app_prospeccao', 
        'app_acaotarefa',
        'app_tarefa',
        'app_servico',
        'app_tiposervico',
        'app_clienteprospect',
        'app_cliente',
    ]
    
    with connection.cursor() as cursor:
        # Desabilita verificação de chaves estrangeiras temporariamente
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        for tabela in tabelas_para_limpar:
            try:
                cursor.execute(f"DELETE FROM {tabela};")
                print(f"✓ Tabela {tabela} limpa")
            except Exception as e:
                print(f"✗ Erro ao limpar {tabela}: {e}")
        
        # Reabilita verificação de chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Reseta os contadores de auto-incremento
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('app_meta', 'app_acaoprospeccao', 'app_prospeccao', 'app_acaotarefa', 'app_tarefa', 'app_servico', 'app_tiposervico', 'app_clienteprospect', 'app_cliente');")
            print("✓ Contadores de ID resetados")
        except Exception as e:
            print(f"Aviso: {e}")
    
    print("\n" + "="*50)
    print("Banco de dados limpo! Usuários e profiles mantidos.")
    print("="*50)

if __name__ == '__main__':
    confirmacao = input("ATENÇÃO: Isso irá APAGAR todos os dados (exceto usuários)!\nDigite 'SIM' para confirmar: ")
    if confirmacao.upper() == 'SIM':
        limpar_banco()
    else:
        print("Operação cancelada.")
