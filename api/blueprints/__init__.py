from api.blueprints.auto import blueprint_auto


list_of_blueprints = [
    (blueprint_auto, '/auto'),
]

__all__ = [
    "list_of_blueprints",
]
