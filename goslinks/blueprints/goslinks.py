from flask import Blueprint, redirect, render_template, url_for

from goslinks.auth.decorators import login_required
from goslinks.auth.utils import logged_in_user
from goslinks.db.factory import get_model
from goslinks.forms import LinkEditForm
from goslinks.helpers.slug import clean_to_slug

bp = Blueprint("goslinks", __name__)


@bp.route("/favicon.ico")
def favicon():
    return "", 204


@bp.route("/")
def home():
    user = logged_in_user()
    if user:
        return redirect(url_for(".edit"))
    else:
        return render_template("home.html")


@bp.route("/edit/", defaults={"slug": ""}, methods=("GET", "POST"))
@bp.route("/edit/<slug>", methods=("GET", "POST"))
@login_required
def edit(slug):
    clean_slug = clean_to_slug(slug)
    user = logged_in_user()
    link_model = get_model("link")
    link = link_model.get_or_init(user, clean_slug)

    form = LinkEditForm(obj=link)
    if form.validate_on_submit():
        new_slug = form.data["slug"]
        link.name = link_model.name_from_organization_and_slug(
            user.organization, new_slug
        )
        link.url = form.data["url"]
        link.save()
        return redirect(url_for(".goslink_redirect", slug=new_slug))
    return render_template("edit.html", user=user, link=link, form=form)


@bp.route("/<path:slug>/")
@login_required
def goslink_redirect(slug):
    clean_slug = clean_to_slug(slug)
    if clean_slug.startswith("edit"):
        return redirect(url_for(".edit", slug=clean_slug[4:]))

    user = logged_in_user()
    link_model = get_model("link")
    try:
        link = link_model.get_from_organization_and_slug(user.organization, clean_slug)
    except link_model.DoesNotExist:
        return redirect(url_for(".edit", slug=clean_slug))
    else:
        return redirect(link.url)
