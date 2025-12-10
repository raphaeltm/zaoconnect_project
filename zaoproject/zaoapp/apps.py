from django.apps import AppConfig


class ZaoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zaoapp'

    def ready(self):
        import zaoapp.signals
