from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired
from flask_share import Share
from app import app



class share_form(FlaskForm):
    blog = StringField()



