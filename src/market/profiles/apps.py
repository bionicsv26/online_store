from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.profiles'

    def ready(self):
        from .signals import save_profile, create_profile
