from api.blueprints.auto import blueprint_auto
from api.blueprints.view_scenarios import blueprint_view
from api.blueprints.create_scenario import blueprint_create


list_of_blueprints = [
    (blueprint_auto, '/auto'),
    (blueprint_view, '/view'),
    (blueprint_create, '/create')
]

__all__ = [
    "list_of_blueprints",
]
