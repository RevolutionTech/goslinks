import functools

from flask import make_response, redirect, url_for

from goslinks.google_oauth2.utils import logged_in_user


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
            return redirect(url_for("google_oauth2.login"))

    return login_required_impl
