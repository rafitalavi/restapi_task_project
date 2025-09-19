from django.apps import AppConfig

class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'

    def ready(self):
        # Import signals so they get registered
        import task.signals
