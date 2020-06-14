import functools

from flask import make_response, redirect, request, session, url_for

from goslinks.auth.constants import AUTH_NEXT_URL_KEY
from goslinks.auth.utils import logged_in_user


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return functools.update_wrapper(no_cache_impl, view)


def login_required(view):
    @functools.wraps(view)
    def login_required_impl(*args, **kwargs):
        if logged_in_user():
            return view(*args, **kwargs)
        else:
            # Save the URL that the user was trying to navigate to
            # as part of the session
            session[AUTH_NEXT_URL_KEY] = request.path

            login_url = url_for("loginpass.login", name="google")
            return redirect(login_url)

    return login_required_impl
