from models import BMI
from app import db, app
from flask_login import current_user,login_required
from BMI.forms import BMIForm, BMIResultForm
from flask import Blueprint, render_template
from users.views import requires_roles
from BMI.calc_bmi import bmi_calc, weight_kg, height_m

# CONFIG
BMI_blueprint = Blueprint('BMI', __name__, template_folder='templates/features')

@BMI_blueprint.route('/bmi', methods=['GET', 'POST'])
@login_required
@requires_roles('user')
def bmi():
    form = BMIForm()
    r_form = BMIResultForm()
    if form.validate_on_submit():
        #gets the units for the height and weight from the form
        h_choice = form.h_units.data
        w_choice = form.w_units.data
        #gets the value for the height and weight from the form, making them a float type
        H = float(form.height.data)
        W = float(form.weight.data)
        #calls the functions to return the height in metres and weight in kg so this can be saved in the database
        weight = weight_kg(W, w_choice)
        height = height_m(H, h_choice)
        #calculates the bmi and saves it to the bmi result form
        r_form.bmi.data = bmi_calc(H, W, h_choice, w_choice)


        with app.app_context():
            #saves the users id, bmi, height and weight in the database
            new_bmi = BMI(user_id=current_user.id, bmi=r_form.bmi.data, height=height, weight=weight)
            db.session.add(new_bmi)
            db.session.commit()

        #redirects the user to the bmi result page with their bmi displayed on it
        return render_template('features/trackers/bmi_result.html', form=r_form, bmi=r_form.bmi.data)

    #reloads the page and the form if the form doesnt validate
    return render_template('features/trackers/bmi.html', form=form)