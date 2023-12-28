import json
import os
import shlex
import subprocess
from typing import Optional, Dict

from django.apps import apps


def create_fixture_permissions(save_file: bool) -> Optional[bytes]:
    """Creates a fixture with permissions"""

    cmd: str = 'django-admin dumpdata --indent 4 auth.permission'
    args: list[str] = shlex.split(cmd)
    proc = subprocess.run(args, stdout=subprocess.PIPE)

    if save_file:
        with open('src/market/fixtures/permissions.json', 'wb') as file:
            file.write(proc.stdout)
    else:
        new_json = proc.stdout
        return new_json


def create_fixture_user_groups() -> None:
    """Creates a fixture with user groups"""

    cmd: str = 'django-admin dumpdata --indent 4 auth.group'
    args: list[str] = shlex.split(cmd)
    proc = subprocess.run(args, stdout=subprocess.PIPE)

    if proc.stdout != b'[\n]\n':
        with open('src/market/fixtures/user_groups.json', 'wb') as file:
            file.write(proc.stdout)
    else:
        basic_group = """[
    {
        "model": "auth.group",
        "pk": 1,
        "fields": {
            "name": "Customer",
            "permissions": []
        }
    },
    {
        "model": "auth.group",
        "pk": 2,
        "fields": {
            "name": "Moderator",
            "permissions": []
        }
    },
    {
        "model": "auth.group",
        "pk": 3,
        "fields": {
            "name": "Administrator",
            "permissions": []
        }
    }
    ]
    
    """
        with open('src/market/fixtures/user_groups.json', 'w') as file:
            file.write(basic_group)


def checking_for_permissions_updates() -> bool:
    """Checks if there have been permission updates"""

    if os.path.isfile('market/fixtures/permissions.json'):
        with open('src/market/fixtures/permissions.json', 'rb') as file:
            old_fixture = file.read()
    else:
        create_fixture_permissions(save_file=True)
        return False

    new_fixture = create_fixture_permissions(save_file=False)

    if old_fixture != new_fixture:
        create_fixture_permissions(save_file=True)
        return False
    return True


def update_user_groups_permissions(sender, **kwargs):
    """"Updates a fixture with users permissions"""

    if not checking_for_permissions_updates():
        with (open('src/market/fixtures/permissions.json', 'r') as file):
            file_json = json.load(file)
            permission_id: Dict = {elem["fields"]["codename"]: elem["pk"] for elem in file_json}
            models = apps.get_models()
            user_group_permissions: Dict = dict()

            for model in models:
                if model.__name__ not in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'User']:
                    for user_group in ('Customer', 'Administrator', 'Moderator'):
                        if hasattr(model._meta, 'permissions_model'):
                            if model._meta.permissions_model.get(user_group) is not None:
                                for perm in model._meta.permissions_model.get(user_group):
                                    user_group_permissions[user_group] = user_group_permissions.get(user_group, []) + [
                                        permission_id[perm]]

        if not os.path.isfile('src/market/fixtures/user_groups.json'):
            create_fixture_user_groups()
        with open('src/market/fixtures/user_groups.json', 'r') as file:
            file_json = json.load(file)

        for elem in file_json:
            for key, value in user_group_permissions.items():
                if elem["fields"]["name"] == key:
                    elem["fields"]["permissions"] = value

        with open('src/market/fixtures/user_groups.json', 'w') as file:
            json.dump(file_json, file, indent=4)
