from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError

class CounterForm(FlaskForm):

    #makes sure the input is a float field and gives an error message if not
    def check_input(self, field):
        try:
            float(field.data)
        except:
            raise ValidationError("Value must be a float or integer")

    # declaration and validation for each input field
    entry_date = DateField(validators=[DataRequired()])
    calories = StringField(validators=[DataRequired(), check_input])

class CounterResult(FlaskForm):
    # declaration for each field
    submit = SubmitField('OK')

class CalCalcForm(FlaskForm):

    # makes sure the input is a float field and gives an error message if not
    def check_input(self, field):
        try:
            float(field.data)
        except:
            raise ValidationError("Value must be a float or integer")

    # declaration and validation for each input field
    protein = StringField(validators=[DataRequired(), check_input])
    fat = StringField(validators=[DataRequired(), check_input])
    carbohydrate = StringField(validators=[DataRequired(), check_input])
    submit = SubmitField('Calculate Calories')

class CalcResultForm(FlaskForm):

    # declaration for each input field
    calories = StringField()
    submit = SubmitField('OK')