# IMPORTS
from flask import Blueprint, render_template
from models import User
from users.views import requires_roles


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@requires_roles('admin')
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/view_all_users', methods=['POST'])
@requires_roles('admin')
def view_all_users():
    current_users = User.query.filter_by(role='user').all()

    return render_template('admin/admin.html', current_users=current_users)


@admin_blueprint.route('/logs', methods=['POST'])
@requires_roles('admin')
def logs():
    with open("health.log", "r") as f:
        content = f.read().splitlines()[-10:]
        content.reverse()

    return render_template('admin/admin.html', logs=content)
