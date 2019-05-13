import functools
import importlib

from flask import current_app

from goslinks.db.models import MODEL_REGISTRY


class ModelNotRegistered(Exception):
    pass


def get_model_base_class():
    model_class_path = current_app.config["MODEL_BASE_CLASS"]
    module_name, class_name = model_class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def create_model_class(model_mixin):
    model_base_class = get_model_base_class()
    model_mixin_meta = type("Meta", (model_mixin.Meta,), {})
    model = type(
        model_mixin.__name__,
        (model_mixin, model_base_class),
        {"Meta": model_mixin_meta},
    )
    return model


@functools.lru_cache(maxsize=None)  # always return the same model class
def get_model(name):
    try:
        model_mixin = MODEL_REGISTRY[name]
    except KeyError:
        raise ModelNotRegistered(f"No model registered by name {name}")
    return create_model_class(model_mixin)
