from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class EnvDescriptionForm(FlaskForm):
    env_description= TextAreaField("env_description",validators=[DataRequired()], render_kw={"placeholder": "Hey! Please try an environment description here..."})
    submit=SubmitField("GENERATE FLOW")



