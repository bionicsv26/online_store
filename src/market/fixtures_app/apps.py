from django.apps import AppConfig
from django.db.models.signals import post_migrate
from market.fixtures_app.signals import update_user_groups_permissions


class FixturesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fixtures_app'

    def ready(self):
        post_migrate.connect(update_user_groups_permissions, sender=self)
