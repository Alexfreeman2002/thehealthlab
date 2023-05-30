"""
Users Views

This file defines a Flask blueprint for handling user-related functionalities
such as registration, login, logout, and account management, including authentication
and role-based access control.
"""


from flask import Blueprint, render_template, flash, redirect, url_for, session, Markup, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db, log_event
from models import User
from users.forms import LoginForm, RegisterForm
from functools import wraps
from datetime import datetime
import bcrypt
import pyotp

users_blueprint = Blueprint('users', __name__, template_folder='templates')


def requires_roles(*roles):
    """
    Decorator that checks if the current user has the required roles.

    Args:
        *roles: Variable number of role strings.

    Returns:
        function:   The wrapped function if the user has the required roles,
                    otherwise renders the '403.html' template.
    """
    def wrapper(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            if current_user.is_anonymous:
                return render_template('403.html')
            elif current_user.role not in roles:
                return render_template('403.html')
            return function(*args, **kwargs)
        return wrapped
    return wrapper


def attempts_reached():
    """
    Checks the number of authentication attempts and displays appropriate flash messages.

    Returns:
        bool: True if the number of incorrect login attempts exceeded 3, False otherwise.
    """
    session['authentication_attempts'] += 1

    if session.get('authentication_attempts') >= 3:
        flash(Markup('Number of incorrect login attempts exceeded. '
                     'Please click <a href = "/reset"> here </a> to reset.'))
        return True

    flash('Incorrect login details. '
          '{} login attempts remaining'.format(3 - session.get('authentication_attempts')))

    return False


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles the user registration process.

    Returns:
        redirect or rendered HTML template: If registration is successful, redirects to the login page.
                                            Otherwise, renders the 'users/register.html' template.
    """
    # Checks if user is logged in
    if not current_user.is_anonymous:
        return render_template('403.html')

    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        log_event('USER-REGISTRATION', form.email.data, request.remote_addr)
        session['pinkey'] = new_user.pinkey  # Used to display pinkey once to user

        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the user login process.

    Returns:
        redirect or rendered HTML template: If login is successful, redirects to the appropriate page based on the user's role.
            Otherwise, renders the 'users/login.html' template.
    """
    if not current_user.is_anonymous:
        return render_template('403.html')

    form = LoginForm()

    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            log_event('INVALID-LOGIN', form.email.data, request.remote_addr)
            if attempts_reached():
                # lock out user from attempting to log in
                return render_template('users/login.html')
            return render_template('users/login.html', form=form)

        # if entered password or pin is incorrect
        if not(bcrypt.checkpw(form.password.data.encode('utf-8'), user.password) and
                pyotp.TOTP(user.pinkey).verify(form.pin.data)):

            log_event('INVALID-LOGIN', form.email.data, request.remote_addr)

            if attempts_reached():
                return render_template('users/login.html')
            return render_template('users/login.html', form=form)

        login_user(user)

        user.last_login = user.current_login
        user.current_login = datetime.now()
        db.session.add(user)
        db.session.commit() 

        log_event('USER-LOGIN', current_user.id, current_user.email, request.remote_addr)

        # redirect user to page depending on role
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin'))
        else:
            return redirect(url_for('users.account'))

    return render_template('users/login.html', form=form)


@users_blueprint.route('/reset')
def reset():
    """
    Resets the number of authentication attempts.

    Returns:
        redirect: Redirects to the login page.
    """
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))


@users_blueprint.route('/account')
@login_required
@requires_roles('admin', 'user')
def account():
    """
    Renders the user account page.

    Returns:
        rendered HTML template: Renders the 'users/account.html' template.
    """
    return render_template('users/account.html',
                           id=current_user.id,
                           email=current_user.email,
                           username=current_user.username)


@users_blueprint.route('/logout')
@login_required
def logout():
    """
    Handles the user logout process.

    Returns:
        rendered HTML template: Renders the 'main/index.html' template.
    """
    # Logs when a user has logged out
    log_event('USER-LOG OUT', current_user.id, current_user.email, request.remote_addr)
    logout_user()
    return render_template('main/index.html')
