"""
Script para resetar completamente a tabela app_meta e suas migrations.
"""
import sqlite3
import os

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*50)
print("Reset completo da tabela app_meta...")
print("="*50)

# 1. DROP da tabela app_meta (caso exista)
try:
    cursor.execute("DROP TABLE IF EXISTS app_meta;")
    print("✓ Tabela app_meta removida (se existia)")
except Exception as e:
    print(f"Aviso: {e}")

# 2. Remove a migration 0005 do registro
try:
    cursor.execute("DELETE FROM django_migrations WHERE app='app' AND name LIKE '0005%';")
    print("✓ Migration 0005 removida do registro")
except Exception as e:
    print(f"Aviso: {e}")

conn.commit()
conn.close()

print("\n" + "="*50)
print("PRONTO!")
print("="*50)
