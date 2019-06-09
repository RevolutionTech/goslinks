from flask_wtf import FlaskForm
from wtforms import StringField, validators

from goslinks.helpers.slug import clean_to_slug


class SlugField(StringField):
    def process_data(self, value):
        super().process_data(value)
        if self.data:
            self.data = clean_to_slug(value)

    def process_formdata(self, valuelist):
        super().process_formdata(valuelist)
        self.data = clean_to_slug(self.data)


class LinkEditForm(FlaskForm):
    slug = SlugField("Name", validators=[validators.DataRequired()])
    url = StringField("URL", validators=[validators.DataRequired(), validators.URL()])
