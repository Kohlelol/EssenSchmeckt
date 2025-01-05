from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


class DatabaseConfig(AppConfig):
    name = 'database'

    def ready(self):
        from database import scheduler
        scheduler.start()