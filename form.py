from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class EnvDescriptionForm(FlaskForm):
    env_description= TextAreaField("env_description",validators=[DataRequired()])
    submit=SubmitField("Generate Flow")