from api.blueprints.auto import blueprint_auto
from api.blueprints.view_scenarios import blueprint_view
from api.blueprints.create_scenario import blueprint_create
from api.blueprints.download import blueprint_download


list_of_blueprints = [
    (blueprint_auto, '/auto'),
    (blueprint_view, '/view'),
    (blueprint_create, '/create'),
    (blueprint_download, '/download')
]

__all__ = [
    "list_of_blueprints",
]
