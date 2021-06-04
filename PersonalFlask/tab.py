from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from PersonalFlask.tabs_auth import login_required
from PersonalFlask.db import get_db

bp = Blueprint('tab', __name__, url_prefix='/tab')

@bp.route('/')
def index():
    db = get_db()
    tabs = db.execute(
        'SELECT p.id, title, body, created, artist_id, username'
        ' FROM tabs_post p JOIN tabs_user u ON p.artist_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('tabs_templates/index.html', tabs=tabs)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tabs_post (title, body, artist_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('tab.index'))
    return render_template('tabs_templates/create.html')

def get_tab(id, check_artist=True):
    tab = get_db().execute(
        'SELECT p.id, title, body, created, artist_id, username'
        ' FROM tabs_post p JOIN tabs_user u ON p.artist_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if tab is None:
        abort(404, f"Tab id {id} does not exist")
    if check_artist and tab['artist_id'] != g.user['id']:
        abort(403)
    return tab

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    tab = get_tab(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE tabs_post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('tab.index'))
    return render_template('tabs_templates/update.html', tab=tab)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_tab(id)
    db = get_db()
    db.execute('DELETE FROM tabs_post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tab.index'))