from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField, StringField
from wtforms.validators import DataRequired


# Define the form to input the current period information
class PeriodForm(FlaskForm):
    start_date = DateField(validators=[DataRequired()])
    end_date = DateField(validators=[DataRequired()])
    period_duration = IntegerField('Period duration/ days', validators=[DataRequired()])
    period_cycle = IntegerField('Period cycle/ days', validators=[DataRequired()])
    submit = SubmitField('Track')

# Define the form to display the next period information
class NextPeriodForm(FlaskForm):
    next_start_date = StringField(validators=[DataRequired()])
    next_end_date = StringField(validators=[DataRequired()])
    ovulation = StringField(validators=[DataRequired()])
    submit = SubmitField('OK')

