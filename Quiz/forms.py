from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class QuizForm(FlaskForm):
    """
    Form class for the quiz form.

    Attributes:
        number_of_questions: SelectField to choose the number of questions.
        submit: SubmitField to submit the form.
    """
    number_of_questions = SelectField('Select the number of questions:',
                                      choices=[(str(i), str(i)) for i in range(5, 16)])
    submit = SubmitField('Begin')
