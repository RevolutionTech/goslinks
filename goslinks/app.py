from flask import Flask

from goslinks.auth.loginpass import register_loginpass_blueprint
from goslinks.blueprints import BLUEPRINTS
from goslinks.cli import migrate as migrate_command
from goslinks.config import Config


def create_flask_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.cli.add_command(migrate_command)
    register_loginpass_blueprint(app)
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
    return app


app = create_flask_app(Config)
