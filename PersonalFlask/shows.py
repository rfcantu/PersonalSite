from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from PersonalFlask.shows_auth import login_required
from PersonalFlask.db import get_db

bp = Blueprint('shows', __name__, url_prefix='/shows')

@bp.route('/')
def index():
    return render_template('shows_templates/index.html')