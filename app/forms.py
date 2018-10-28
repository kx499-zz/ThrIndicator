from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from config import VALIDATE
import re


class IndicatorForm(Form):
    value = StringField('Value', validators=[DataRequired()])
    data_type = SelectField('Data Type', validators=[DataRequired()])
    source = SelectField('Source', validators=[DataRequired()])
    direction = SelectField('Direction', validators=[DataRequired()])
    ttl = SelectField('TTL', coerce=int, validators=[DataRequired()])
    details = StringField('Details', widget=TextArea())
    active = BooleanField('Active')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        print self.data_type.data
        rex = VALIDATE.get(self.data_type.data)
        field = self.value
        if rex and not re.search(rex, field.data):
            field.errors.append("Value doesn't match data_type")
            return False
        return True





