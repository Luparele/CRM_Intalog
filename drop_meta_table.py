"""
Script para DROPAR e recriar a tabela app_meta.
Execute: python drop_meta_table.py
"""
import sqlite3
import os

db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"Erro: Banco de dados '{db_path}' não encontrado!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*50)
print("Removendo tabela app_meta completamente...")
print("="*50)

# 1. DROP da tabela app_meta
try:
    cursor.execute("DROP TABLE IF EXISTS app_meta;")
    print("✓ Tabela app_meta removida")
except Exception as e:
    print(f"Erro ao dropar app_meta: {e}")

# 2. Remove do sqlite_sequence
try:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_meta';")
    print("✓ Sequência removida")
except Exception as e:
    pass

# 3. Remove TODAS as migrations do app (vamos aplicar do zero)
try:
    cursor.execute("DELETE FROM django_migrations WHERE app='app';")
    print("✓ Todas as migrations do app removidas do registro")
except Exception as e:
    print(f"Erro: {e}")

conn.commit()
conn.close()

print("\n" + "="*50)
print("PRONTO! Agora execute:")
print("  python manage.py migrate --fake app 0004")
print("  python manage.py makemigrations")
print("  python manage.py migrate")
print("="*50)
