from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .signals import update_user_groups_permissions


class UsersPermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.users_permissions'

    def ready(self):
        post_migrate.connect(update_user_groups_permissions, sender=self)
