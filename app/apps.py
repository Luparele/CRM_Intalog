# app/apps.py
from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # --- INÍCIO DA ALTERAÇÃO ---
    def ready(self):
        # Importa os sinais para que eles sejam registrados quando o Django iniciar.
        import app.models
    # --- FIM DA ALTERAÇÃO ---