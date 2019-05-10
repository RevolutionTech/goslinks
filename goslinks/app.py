from flask import Flask

from goslinks.blueprints import BLUEPRINTS
from goslinks.config import Config


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
    return app


app = create_app(Config)
