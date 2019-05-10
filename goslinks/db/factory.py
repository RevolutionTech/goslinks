import importlib

from flask import current_app


class ModelNotRegistered(Exception):
    pass


def get_model_registry():
    model_registry_path = current_app.config["MODEL_REGISTRY"]
    module_name, registry_name = model_registry_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, registry_name)


def get_model(name):
    model_registry = get_model_registry()
    try:
        return model_registry[name]
    except KeyError:
        raise ModelNotRegistered(f"No model registered by name {name}")
