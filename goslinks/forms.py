from flask_wtf import FlaskForm
from wtforms import StringField, validators


class SlugField(StringField):
    def __init__(self, *args, **kwargs):
        additional_validators = kwargs.pop("validators", None) or []
        kwargs["validators"] = [
            validators.Regexp(
                r"^[-\w]+$",
                message="Only lowercase letters, numbers, and dashes (-) are allowed.",
            )
        ] + additional_validators
        super().__init__(*args, **kwargs)

    def process_data(self, value):
        if value:
            value = value.lower().replace(" ", "-").replace("_", "-")
        return super().process_data(value)


class LinkEditForm(FlaskForm):
    slug = SlugField("Name")
    url = StringField("URL", validators=[validators.DataRequired(), validators.URL()])
