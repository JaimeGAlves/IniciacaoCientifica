from django.apps import AppConfig
from settings.settings import BASE_DIR


class DefaultApp(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.core'
    label = 'core'
    verbose_name = 'Core Application'
    path = BASE_DIR / 'backend' / 'core'