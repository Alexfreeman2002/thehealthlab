from flask import Blueprint, render_template, flash, redirect, url_for, session, Markup, request



share_blueprint = Blueprint('Share', __name__, template_folder='templates/features')

@share_blueprint.route('/share', methods=['GET', 'POST'])
def share_run():
    pass