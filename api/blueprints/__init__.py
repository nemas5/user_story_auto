from api.blueprints.auto import blueprint_auto
from api.blueprints.view_scenarios import blueprint_view
from api.blueprints.create_scenario import blueprint_create
from api.blueprints.download import blueprint_download
from api.blueprints.view_users import blueprint_users


list_of_blueprints = [
    (blueprint_auto, '/auto'),
    (blueprint_view, '/view'),
    (blueprint_create, '/create'),
    (blueprint_download, '/download'),
    (blueprint_users, '/users')
]

__all__ = [
    "list_of_blueprints",
]
