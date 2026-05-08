# salve como gerar_token.py e rode no seu Windows
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Escopo para acesso total ao Drive (apenas para arquivos criados pelo app)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
creds = flow.run_local_server(port=0)

# Salva o token para uso posterior
with open('token.json', 'w') as token:
    token.write(creds.to_json())

print("Sucesso! O arquivo token.json foi criado.")
