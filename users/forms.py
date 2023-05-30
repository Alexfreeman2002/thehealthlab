from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
import re


def name_check(form, field):
    # Special characters not allowed in names
    excluded_characters = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"

    # Loops through every character in the name
    for character in field.data:
        # Checks if character is in the list of excluded_characters
        if character in excluded_characters:
            raise ValidationError(f"Can't Contain {character}")


def password_check(form, field):
    # Passwords must contain a digit, lowercase, uppercase and special character
    password = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')

    # Checks if password does not include correct characters
    if not password.match(field.data):
        raise ValidationError("Must contain at least 1 number, at least 1 lowercase character, "
                              "at least 1 uppercase character, at least 1 special character.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[
        DataRequired(),
        Email()
    ])

    username = StringField(validators=[
        DataRequired(),
        name_check
    ])

    password = PasswordField(validators=[
        DataRequired(),
        Length(min=6, max=12),
        password_check
    ])

    confirm_password = PasswordField(validators=[
        DataRequired(),
        EqualTo('password', message='Both passwords must be equal')
    ])

    submit = SubmitField()


class LoginForm(FlaskForm):
    """
    Represents a login form.

    Attributes:
        email (StringField):            The email field for entering the user's email address.
        password (PasswordField):       The password field for entering the user's password.
        pin (StringField):              The pin field for entering the user's PIN.
        recaptcha (RecaptchaField):     The reCAPTCHA field for verifying user's humanity.
        submit (SubmitField):           The submit button for submitting the form.
    """
    email = StringField(validators=[
        DataRequired(),
        Email(),
    ])

    password = PasswordField(validators=[
        DataRequired(),
    ])

    pin = StringField(validators=[
        DataRequired()
    ])

    recaptcha = RecaptchaField()

    submit = SubmitField()
