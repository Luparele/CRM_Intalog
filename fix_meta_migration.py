"""
Script para limpar a tabela app_meta e o registro de migrations problemáticas.
Execute: python fix_meta_migration.py
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
print("Corrigindo banco de dados...")
print("="*50)

# 1. Limpa a tabela app_meta
try:
    cursor.execute("DELETE FROM app_meta;")
    print("✓ Tabela app_meta limpa")
except Exception as e:
    print(f"Aviso app_meta: {e}")

# 2. Reseta o contador de ID
try:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_meta';")
    print("✓ Contador de ID resetado")
except Exception as e:
    print(f"Aviso sequence: {e}")

# 3. Remove registros de migrations problemáticas
try:
    cursor.execute("""
        DELETE FROM django_migrations 
        WHERE app='app' 
        AND name LIKE '%meta%cliente%'
    """)
    print("✓ Migrations problemáticas removidas do registro")
except Exception as e:
    print(f"Aviso migrations: {e}")

# 4. Lista migrations restantes
print("\nMigrations registradas para 'app':")
cursor.execute("SELECT name FROM django_migrations WHERE app='app' ORDER BY name;")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

conn.commit()
conn.close()

print("\n" + "="*50)
print("PRONTO! Agora execute:")
print("  python manage.py makemigrations")
print("  python manage.py migrate")
print("="*50)
