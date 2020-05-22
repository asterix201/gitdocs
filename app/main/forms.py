from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    project = StringField('Git project name', validators=[DataRequired()])
    submit = SubmitField('Register')
