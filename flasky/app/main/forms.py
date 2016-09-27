from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NameForm(Form):
    name = TextAreaField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
