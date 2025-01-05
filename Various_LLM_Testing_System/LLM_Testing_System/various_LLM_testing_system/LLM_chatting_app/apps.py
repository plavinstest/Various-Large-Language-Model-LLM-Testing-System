from django.apps import AppConfig

class LlmChatingAppConfig(AppConfig):
    # Specifying the default auto field for primary keys in the app
    default_auto_field = "django.db.models.BigAutoField"
    # Define the name of the Django application
    name = "LLM_chatting_app"
