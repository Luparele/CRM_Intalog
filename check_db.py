import sqlite3

conn = sqlite3.connect(r'C:\Users\Segurança\Documents\CRM Intalog\db.sqlite3')
cursor = conn.cursor()

cursor.execute("""
    SELECT u.id, u.username, u.first_name, u.last_name, p.setor 
    FROM auth_user u 
    LEFT JOIN app_profile p ON u.id = p.user_id 
    ORDER BY u.username
""")

print("=" * 70)
print("LISTA DE USUÁRIOS")
print("=" * 70)
print(f"{'ID':<5} {'Username':<20} {'Nome':<25} {'Setor':<15}")
print("-" * 70)

for row in cursor.fetchall():
    user_id, username, first_name, last_name, setor = row
    nome = f"{first_name or ''} {last_name or ''}".strip()
    print(f"{user_id:<5} {username:<20} {nome:<25} {setor or 'NULL':<15}")

print("=" * 70)
conn.close()
