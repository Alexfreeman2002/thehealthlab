from app import db, app
from datetime import datetime
from flask_login import UserMixin
import pyotp, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    pinkey = db.Column(db.String(100), nullable=False)

    # User information
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    # Event logging
    registered_on = db.Column(db.DateTime, nullable=False)
    current_login = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

    # Average user quiz score
    average_quiz_score = db.Column(db.Float, nullable=True)

    # Define the relationship to other tables
    bmi = db.relationship('BMI')
    period = db.relationship('Period')
    calories = db.relationship('Calories')

    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.pinkey = pyotp.random_base32()
        self.registered_on = datetime.now()
        self.current_login = None
        self.last_login = None

class BMI(db.Model):
    __tablename__ = 'bmi'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # User BMI information
    bmi = db.Column(db.Double, nullable=False)
    height = db.Column(db.Double, nullable=False)
    weight = db.Column(db.Double, nullable=False)

    def __init__(self, user_id, bmi, height, weight):
        self.user_id = user_id
        self.bmi = bmi
        self.height = height
        self.weight = weight

#change later
class Period(db.Model):
    __tablename__ = 'period'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # User current period information
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    period_duration = db.Column(db.Integer, nullable=False)
    period_cycle = db.Column(db.Integer, nullable=False)
    # User next period predicted information
    next_start_date = db.Column(db.DateTime, nullable=False)
    next_end_date = db.Column(db.DateTime, nullable=False)
    ovulation = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, start_date, end_date, period_duration, period_cycle, next_start_date, next_end_date, ovulation):
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.period_duration = period_duration
        self.period_cycle = period_cycle
        self.next_start_date = next_start_date
        self.next_end_date = next_end_date
        self.ovulation = ovulation


class Calories(db.Model):
    __tablename__ = 'calories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # User calories information
    entry_name = db.Column(db.Date, nullable=False)
    daily_calories = db.Column(db.Double, nullable=False)

    def __init__(self, user_id, entry_name, daily_calories):
        self.user_id = user_id
        self.entry_name = entry_name
        self.daily_calories = daily_calories

class CalorieGoal(db.Model):
    __tablename__ = 'calorie_goal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # User calories information
    calorie_goal = db.Column(db.Double, nullable=False)

    def __init__(self, user_id, calorie_goal):
        self.user_id = user_id
        self.calorie_goal = calorie_goal

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)

    # Multiple choice question
    question = db.Column(db.String, nullable=False, unique=True)

    # Possible answers for multiple choice question
    answer_one = db.Column(db.String, nullable=False)
    answer_two = db.Column(db.String, nullable=False)
    answer_three = db.Column(db.String, nullable=False)
    answer_four = db.Column(db.String, nullable=False)

    # Correct answer to multiple choice question
    correct_answer = db.Column(db.Integer, nullable=False)

    def __init__(self, question, one, two, three, four, answer):
        self.question = question
        self.answer_one = one
        self.answer_two = two
        self.answer_three = three
        self.answer_four = four
        self.correct_answer = answer


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # For now there will be max 15 questions for each category
        q = Question(question="What does BMI stand for?",
                                     one="Body Mass Index",
                                     two="Basic Metabolic Indicator",
                                     three="Balanced Muscle Index",
                                     four="Body Measurement Index",
                                     answer=1)
        db.session.add(q)
        q = Question(
            question="Which of the following is a measure of body fat based on height and weight?",
            one="VO2 max",
            two="BMR",
            three="BMI",
            four="RMR",
            answer=3)
        db.session.add(q)
        q = Question(question="Which macronutrient provides the most calories per gram?",
                                     one="Protein",
                                     two="Carbohydrates",
                                     three="Fats",
                                     four="Fiber",
                                     answer=3)
        db.session.add(q)
        q = Question(
            question="Which of the following diet plans focuses on reducing carbohydrate intake?",
            one="Mediterranean diet",
            two="Ketogenic diet",
            three="Vegan diet",
            four="Dash diet",
            answer=2)
        db.session.add(q)
        q = Question(question="How many calories are in one gram of carbohydrates?",
                                     one="4 calories",
                                     two="7 calories",
                                     three="9 calories",
                                     four="12 calories",
                                     answer=1)
        db.session.add(q)
        q = Question(
            question="What is the term for the number of calories the body needs to maintain basic bodily functions at rest?",
            one="RMR (Resting Metabolic Rate)",
            two="TDEE (Total Daily Energy Expenditure)",
            three="BMR (Basal Metabolic Rate)",
            four="VO2 max",
            answer=1)
        db.session.add(q)
        q = Question(question="Which of the following is a measure of cardiorespiratory fitness?",
                                     one="1RM (One Repetition Maximum)",
                                     two="VO2 max",
                                     three="BMI",
                                     four="RHR (Resting Heart Rate)",
                                     answer=2)
        db.session.add(q)
        q = Question(
            question="Which of the following is a high-intensity interval training (HIIT) exercise?",
            one="Jogging",
            two="Cycling",
            three="Burpees",
            four="Yoga",
            answer=3)
        db.session.add(q)
        q = Question(
            question="What is the recommended amount of exercise per week for adults, according to health guidelines?",
            one="60 minutes",
            two="150 minutes",
            three="300 minutes",
            four="500 minutes",
            answer=2)
        db.session.add(q)
        q = Question(question="How many calories are in one gram of fat?",
                                      one="4 calories",
                                      two="7 calories",
                                      three="9 calories",
                                      four="12 calories",
                                      answer=3)
        db.session.add(q)
        q = Question(question="Which of the following is a measure of muscular strength?",
                                      one="BMI",
                                      two="VO2 max",
                                      three="1RM (One Repetition Maximum)",
                                      four="RHR (Resting Heart Rate)",
                                      answer=3)
        db.session.add(q)
        q = Question(question="Which of the following nutrients is a micronutrient?",
                                      one="Protein",
                                      two="Carbohydrates",
                                      three="Fats",
                                      four="Vitamins",
                                      answer=4)
        db.session.add(q)
        q = Question(
            question="Which of the following is a tool used for tracking daily caloric intake and expenditure?",
            one="Pedometer",
            two="BMI calculator",
            three="Food diary",
            four="Heart rate monitor",
            answer=3)
        db.session.add(q)
        q = Question(
            question="What is the term for the amount of energy needed to raise the temperature of 1 kilogram of water by 1 degree Celsius?",
            one="Calorie",
            two="Metabolism",
            three="Kilocalorie",
            four="Macronutrient",
            answer=3)
        db.session.add(q)
        q = Question(
            question="What is the recommended daily calorie intake for an average adult, depending on factors like age, gender, and activity level?",
            one="1,000-1,200 calories",
            two="1,500-1,800 calories",
            three="2,000-2,500 calories",
            four="3,000-3,500 calories",
            answer=3)
        db.session.add(q)


        admin = User(email='admin@email.com',
                     password='Admin1!',
                     username='johnsmith2',
                     role='admin')

        db.session.add(admin)
        db.session.commit()