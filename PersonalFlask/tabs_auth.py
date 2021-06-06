import functools 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from PersonalFlask.db import get_db

bp = Blueprint('tabs_auth', __name__, url_prefix='/tabs_auth')

@bp.route('register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        # Check for arguments submittied in the form
        # And then check username and email are unique
        if not username:
            error = 'Username is required'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM tabs_user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered"
        elif db.execute(
            'SELECT id FROM tabs_user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = f"Email {email} is already registered"
        
        # Check if error was thrown
        if error is None:
            db.execute(
                'INSERT INTO tabs_user (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('tabs_auth.login'))
        flash(error)
    return render_template('tabs_auth_templates/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM tabs_user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('tabs_index'))
        flash(error)
    return render_template('tabs_auth_templates/login.html')

'''
Check if session has a user id
Lasts for length of request
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM tabs_user WHERE id = ?', (user_id,)
        ).fetchone()

'''
To logout just clear the session and redirect to home page
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('tab.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('tabs_auth.login'))
        return view(**kwargs)
    return wrapped_view