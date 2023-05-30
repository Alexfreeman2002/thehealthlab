import os
import logging
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_talisman import Talisman


# Custom filter for logging
class SecurityFilter(logging.Filter):
    def filter(self, record):
        """Return log record if it contains the specified string"""
        return 'SECURITY-EVENT' in record.getMessage()


def log_event(event_type, *user_data):
    """Log custom record with given event type and user data"""
    logging.warning('SECURITY-EVENT - %s [%s]', event_type, str(user_data))


# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Set up file handler for storing log events
file_handler = logging.FileHandler('health.log', 'a')
file_handler.setLevel(logging.WARNING)
file_handler.addFilter(SecurityFilter())

# Set up log event formatter
formatter = logging.Formatter('%(asctime)s : %(message)s', '%d/%m/%Y %I:%M:%S %p')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO') == 'true'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'true'
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# Initialize database
db = SQLAlchemy(app)

# Content Security Policy (CSP) configuration
csp = {
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://www.england.nhs.uk/feed/',
        'https://www.google.com/recaptcha/',
        'https://www.gstatic.com/recaptcha/'
    ]
}

talisman = Talisman(app, content_security_policy=csp)

@app.route('/')
def index():
    """Home page view"""
    return render_template('main/index.html')

# BLUEPRINTS
from users.views import users_blueprint
from BMI.views import BMI_blueprint
from PeriodTracker.views import period_blueprint
from CalorieCounter.views import calorie_blueprint
from Quiz.views import quiz_blueprint
from admin.views import admin_blueprint
from RSS.views import news_blueprint
from SearchDiseases.views import search_blueprint
from health.views import health_blueprint

# Register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(BMI_blueprint)
app.register_blueprint(period_blueprint)
app.register_blueprint(calorie_blueprint)
app.register_blueprint(quiz_blueprint)
app.register_blueprint(news_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(health_blueprint)


# LOGIN MANAGER
from models import User
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))


# Error handlers
@app.errorhandler(400)
def bad_request_error(error):
    """Error handler for 400 - Bad Request"""
    return render_template('400.html'), 400


@app.errorhandler(403)
def forbidden_error(error):
    """Error handler for 403 - Forbidden"""
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    """Error handler for 404 - Not Found"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Error handler for 500 - Internal Server Error"""
    return render_template('500.html'), 500


@app.errorhandler(503)
def service_unavailable_error(error):
    """Error handler for 503 - Service Unavailable"""
    return render_template('503.html'), 503


if __name__ == "__main__":
    app.run()
