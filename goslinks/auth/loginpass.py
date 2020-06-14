from authlib.integrations.flask_client import OAuth
from flask import redirect, render_template, session
from loginpass import Google, create_flask_blueprint

from goslinks.auth.constants import AUTH_EMAIL_KEY, AUTH_NEXT_URL_KEY
from goslinks.db.factory import get_model


def handle_authorize(_remote, _token, user_info):
    is_email_verified = user_info.get("email_verified", False)
    if "hd" not in user_info or not is_email_verified:
        return render_template("google_oauth2_error.html"), 401

    user = get_model("user").update_or_create_user(user_info)
    session[AUTH_EMAIL_KEY] = user.email

    next_url = session.pop(AUTH_NEXT_URL_KEY, "/")
    return redirect(next_url, code=302)


def register_loginpass_blueprint(app):
    oauth = OAuth(app)
    oauth_bp = create_flask_blueprint([Google], oauth, handle_authorize)
    app.register_blueprint(oauth_bp)
