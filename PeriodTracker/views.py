import datetime
from datetime import timedelta
from app import db
from models import Period
from PeriodTracker.forms import PeriodForm
from PeriodTracker.forms import NextPeriodForm
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from users.views import requires_roles

# Define the name of blueprint and get the path of template
period_blueprint = Blueprint('period_tracker', __name__, template_folder='templates/features')


# Add the route of blueprint and define the methods
@period_blueprint.route('/period_tracker', methods=['GET', 'POST'])
# Only logged-in users can access
@login_required
# Add RBAC to make this feature only can be accessed by user role
@requires_roles('user')
# Define the period tracker function
def period_tracker():
    # Define the forms for input info and display result
    p_form = PeriodForm()
    r_form = NextPeriodForm()
    # If user submit the period information form
    if p_form.validate_on_submit():
        # Get the current period info from the period form
        start_date = p_form.start_date.data
        end_date = p_form.end_date.data
        period_duration = p_form.period_duration.data
        period_cycle = p_form.period_cycle.data
        # Call the calculate function to get the calculated results
        next_start_date, next_end_date, ovulation = calculate_next_period(start_date, end_date, period_duration,
                                                                          period_cycle)

        # Set the next period info to the next period form
        r_form.next_start_date.data = next_start_date
        r_form.next_end_date.data = next_end_date
        r_form.ovulation.data = ovulation

        # Store the period information to the database
        period = Period(user_id=current_user.id, start_date=start_date, end_date=end_date,
                        period_duration=period_duration, period_cycle=period_cycle, next_start_date=next_start_date,
                        next_end_date=next_end_date, ovulation=ovulation)
        db.session.add(period)
        db.session.commit()

        # If the form submit, redirect users to the period_result template to display the result
        return render_template('features/trackers/period_result.html', form=r_form,
                               next_start_date=r_form.next_start_date.data, next_end_date=r_form.next_start_date.data,
                               ovulation=r_form.next_start_date.data)

    # Redirect users to the period template for the next calculate
    return render_template('features/trackers/period.html', form=p_form)


# Only logged-in users can access
@login_required
# Add RBAC to make this feature only can be accessed by user role
@requires_roles('user')
# Define the function to calculate next period
def calculate_next_period(start_date, end_date, period_duration, period_cycle):
    next_start_date = start_date + timedelta(days=period_cycle)
    next_end_date = end_date + timedelta(days=period_cycle)
    ovulation = next_start_date - timedelta(days=14)
    return next_start_date, next_end_date, ovulation
