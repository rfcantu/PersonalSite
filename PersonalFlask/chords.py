from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from PersonalFlask.tabs_auth import login_required
from PersonalFlask.db import get_db

import requests

bp = Blueprint('chords', __name__)

@bp.route('/chords', methods=('GET', 'POST'))
def chord():
    r = None
    if request.method == 'POST':
        root = request.form['root']
        quality = request.form['quality']
        tension = request.form['tension']
        bass = request.form['bass']
        error = None
        db = get_db()

        if not root:
            error = "Root note is required"
        
        chord = f"{root}_{quality}{tension}{bass}"
        payload = {'nameLike': chord}
        r = requests.get("https://api.uberchord.com/v1/chords", params=payload).json()
    return render_template('tabs_templates/chords.html', resp=r)