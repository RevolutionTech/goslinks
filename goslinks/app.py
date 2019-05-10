from flask import Flask

from goslinks.blueprints import BLUEPRINTS

app = Flask(__name__)
app.config.from_object("goslinks.config.Config")
for bp in BLUEPRINTS:
    app.register_blueprint(bp)
