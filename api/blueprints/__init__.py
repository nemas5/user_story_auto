from api.blueprints.auto import blueprint_auto
from api.blueprints.view_scenarios import blueprint_sc_view
from api.blueprints.create_scenario import blueprint_create


list_of_blueprints = [
    (blueprint_auto, '/auto'),
    (blueprint_sc_view, '/sc_view'),
    (blueprint_create, '/create')
]

__all__ = [
    "list_of_blueprints",
]
