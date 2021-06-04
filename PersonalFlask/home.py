import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from PersonalFlask.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('home_templates/index.html')

@bp.route('/projects', methods=('GET',))
def projects():
    return render_template('home_templates/projects.html')

@bp.route('/contact', methods=('GET',))
def contact():
    return render_template('home_templates/contact.html')

@bp.route('/unity', methods=('GET',))
def unity():
    return render_template('home_templates/unity.html')