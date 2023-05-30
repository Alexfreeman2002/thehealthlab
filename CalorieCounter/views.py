from app import db, app
from models import Calories, CalorieGoal
from CalorieCounter.forms import CalCalcForm, CounterForm, CalcResultForm, CounterResult
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from users.views import requires_roles
from CalorieCounter.calc_cals import calculate_calories

# CONFIG
calorie_blueprint = Blueprint('calories', __name__, template_folder='templates/features')


@calorie_blueprint.route('/view', methods=['GET', 'POST'])
@login_required
@requires_roles('user')
def calorie_counter():
    form = CounterForm()
    r_form = CounterResult()
    if form.validate_on_submit():
        entry_date = form.entry_date.data
        calories = float(form.calories.data)
        # checks which button is pressed and gives the correct action
        if request.form.get('action') == 'Add to existing entry':
            edit(entry_date, calories)
            return render_template('features/trackers/calorie_counter_result.html', form=r_form)
        elif request.form.get('action') == "Create new entry":
            new_entry(entry_date, calories)
            return render_template('features/trackers/calorie_counter_result.html', form=r_form)
        elif request.form.get('action') == "View all entries":
            view()

    # reloads the page and the form if the form doesnt validate
    return render_template('features/trackers/calorie_counter.html', form=form)


@calorie_blueprint.route('/view_entries', methods=['POST'])
@login_required
@requires_roles('user')
def view():
    form = CounterForm()
    # gets all the entries for the current user id
    entries = Calories.query.filter_by(user_id=current_user.id).all()

    if len(entries) == 0:
        # displays error message if the user has no entries
        flash("You have no calorie data in the database")
        return render_template("features/trackers/error.html")
    else:
        # displays the entries for the user
        return render_template("features/trackers/calorie_counter.html", form=form, entries=entries)


def edit(entry_date, new_entry):
    with app.app_context():
        # loops through the data in the calories table that belongs to the current user and has the given entry date
        for row in db.session.query(Calories).filter_by(user_id=current_user.id, entry_name=entry_date):
            # when it finds this data is takes the calorie value
            existing_cals = row.daily_calories
        # saves this whole row to object
        object = Calories.query.filter_by(user_id=current_user.id, entry_name=entry_date).first()
        # if this object doesnt existing an error message is displayed
        if object == None:
            flash("Date doesn't exist in the database, please try another date or create an entry for this date")
        else:
            # if this object exists, the calories are updated
            db.session.delete(object)
            db.session.commit()
            new_cals = existing_cals + new_entry
            new_cal = Calories(user_id=current_user.id, entry_name=entry_date, daily_calories=new_cals)
            db.session.add(new_cal)
            db.session.commit()
            flash("Your data has been updated successfully")


def new_entry(entry_date, calories):
    with app.app_context():
        # searches the database to see if the entry date for that user already exists
        object = Calories.query.filter_by(user_id=current_user.id, entry_name=entry_date).first()

        if object == None:
            # if there isn't an existing entry with this entry date for this user it will create a new object and add it to the database
            new_cal = Calories(user_id=current_user.id, entry_name=entry_date, daily_calories=calories)
            db.session.add(new_cal)
            db.session.commit()
            flash("Your data has been added to the database successfully")
        else:
            # if there is an existing entry with this entry date the user will be shown an error message
            flash("Date already exists in the database, try adding to this date or creating an entry for another date")


@calorie_blueprint.route('/calculator', methods=['GET', 'POST'])
@login_required
@requires_roles('user')
def calorie_calculator():
    form = CalCalcForm()
    r_form = CalcResultForm()
    if form.validate_on_submit():
        # gets the values for protein, fat and carbohydrates from the user form and gives them the type float
        protein = float(form.protein.data)
        fat = float(form.fat.data)
        carbs = float(form.carbohydrate.data)

        # calculates the total calories given their inputs
        total_cals = calculate_calories(protein, fat, carbs)

        # saves this value to the form for the results page
        r_form.calories.data = total_cals

        with app.app_context():
            # cerates a new object with the users calories and saves it to  the database
            new_cal = CalorieGoal(user_id=current_user.id, calorie_goal=total_cals)
            db.session.add(new_cal)
            db.session.commit()

        # redirects the user to the calculation result with the result form and the calculated calories for the user
        return render_template('features/trackers/calc_result.html', form=r_form, calories=r_form.calories.data)
    # if the form doesn't validate, the page is reloaded with the original form
    return render_template('features/trackers/calories.html', form=form)
