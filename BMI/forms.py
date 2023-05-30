from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, ValidationError


class BMIForm(FlaskForm):

    #makes sure the input is a float field and gives an error message if not
    def check_input(self, field):
        try:
            float(field.data)
        except:
            raise ValidationError("Value must be a float or integer")

    #makes sure the units for the height is correct
    def check_h_choice(self, field):
        h_choice = field.data
        while h_choice.upper() != "CM" and h_choice.upper() != "FEET":
            raise ValidationError("Value must be either cm or feet")

    #makes sure the units for the weight is correct
    def check_w_choice(self, field):
        w_choice = field.data
        while w_choice.upper() != "KG" and w_choice.upper() != "LBS":
            raise ValidationError("Value must be either kg or lbs")

    # declaration and validation for each input field
    height = StringField(validators=[DataRequired(), check_input])
    h_units = StringField(validators=[DataRequired(), check_h_choice])
    weight = StringField(validators=[DataRequired(), check_input])
    w_units = StringField(validators=[DataRequired(), check_w_choice])
    submit = SubmitField('Calculate')

class BMIResultForm(FlaskForm):

    # declaration for each field
    bmi = FloatField()
    submit = SubmitField('OK')