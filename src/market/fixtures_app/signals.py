import ast
import os
import shlex
import subprocess
from typing import List, Optional

from market.market.settings import INSTALLED_APPS


def search_for_model_names(root: str) -> List[str]:
    """Search model names for the current app"""

    abspath_models_py: str = os.path.join(root, 'models.py')
    model_names: list = []
    for im in ast.walk(ast.parse(open(abspath_models_py).read())):
        if isinstance(im, ast.ClassDef) and not im.name.lower() == 'meta':
            model_names.append(im.name.lower())
    return model_names


def create_fixtures_permissions(save_file: bool) -> Optional[bytes]:
    """Creates a fixture with permissions"""

    cmd = 'django-admin dumpdata --indent 4 auth.permission'
    args = shlex.split(cmd)
    proc = subprocess.run(args, stdout=subprocess.PIPE)

    if save_file:
        with open('market/fixtures/permissions.json', 'wb') as file:
            file.write(proc.stdout)
    else:
        new_json = proc.stdout
        return new_json


def checking_for_permissions_updates() -> bool:
    """Checks if there have been permission updates"""

    if os.path.isfile('market/fixtures/permissions.json'):
        with open('market/fixtures/permissions.json', 'rb') as file:
            old_json = file.read()
            print(old_json)
    else:
        create_fixtures_permissions(save_file=True)
        return False

    new_json = create_fixtures_permissions(save_file=False)

    print(new_json)
    print(old_json == new_json)
    return old_json == new_json


def update_user_groups_permissions(sender, **kwargs):
    if not checking_for_permissions_updates():
        print(INSTALLED_APPS)
        list_apps = [app.split('.')[0] for app in INSTALLED_APPS if not app.startswith('django.')]
        print(list_apps)

        for app in list_apps:
            root: str = os.path.join(os.getcwd(), app)
            print(root)
            dict_cur_app = {app: search_for_model_names(root)}
            print(dict_cur_app)
