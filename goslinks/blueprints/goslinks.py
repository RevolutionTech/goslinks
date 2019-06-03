from flask import Blueprint, redirect, render_template, url_for

from goslinks.db.factory import get_model
from goslinks.forms import LinkEditForm
from goslinks.google_oauth2.decorators import login_required
from goslinks.google_oauth2.utils import logged_in_user

bp = Blueprint("goslinks", __name__)


@bp.route("/")
def links():
    user = logged_in_user()
    return render_template("links.html", user=user, links=get_model("link").scan())


@bp.route("/edit/", defaults={"slug": ""})
@bp.route("/edit/<slug>", methods=("GET", "POST"))
@login_required
def edit(slug):
    user = logged_in_user()
    link_model = get_model("link")
    link = link_model.get_or_init(user, slug)

    form = LinkEditForm(obj=link)
    if form.validate_on_submit():
        new_slug = form.data["slug"]
        link.name = link_model.name_from_organization_and_slug(
            user.organization, new_slug
        )
        link.url = form.data["url"]
        link.save()
        return redirect(url_for(".goslink_redirect", slug=new_slug))
    return render_template("edit.html", form=form)


@bp.route("/<slug>/")
@login_required
def goslink_redirect(slug):
    user = logged_in_user()
    link_model = get_model("link")
    try:
        link = link_model.get_from_organization_and_slug(user.organization, slug)
    except link_model.DoesNotExist:
        return redirect(url_for(".edit", slug=slug))
    else:
        return redirect(link.url)
