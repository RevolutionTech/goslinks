from flask import session

from goslinks.auth.constants import AUTH_EMAIL_KEY
from goslinks.db.factory import get_model


def logged_in_user():
    email = session.get(AUTH_EMAIL_KEY)
    if email:
        user_model = get_model("user")
        try:
            return user_model.get(email)
        except user_model.DoesNotExist:
            # User has been deleted, remove from session
            session.pop(AUTH_EMAIL_KEY, None)
