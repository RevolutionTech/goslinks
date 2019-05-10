from goslinks.db.models import UserModel, LinkModel


class ModelNotRegistered(Exception):
    pass


MODEL_REGISTRY = {
    "user": UserModel,
    "link": LinkModel,
}


def model_factory(name):
    try:
        return MODEL_REGISTRY[name]
    except KeyError:
        raise ModelNotRegistered(f"No model registered by name {name}")
