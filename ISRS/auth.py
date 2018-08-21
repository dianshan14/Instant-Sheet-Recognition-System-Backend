import functools
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash, g
)
from werkzeug.security import check_password_hash, generate_password_hash
from ISRS.model import db, User
from ISRS.color import colors

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # TODO: 'username' -> form and variable name
        print(request.form)
        username = request.form['username']
        password = request.form['password']

        error_msg = None
        if not username:
            error_msg = 'Username is required'
        elif not password:
            error_msg = 'Password is required'
        elif User.query.filter_by(username=username).first() is not None:
            error_msg = 'User {} is already registered'.format(username)

        if error_msg is None:
            print(len(generate_password_hash(password, 'sha256')))
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            print(colors.GREEN + 'Register success' + colors.END)
            return redirect(url_for('auth.login'))
        
        flash(error_msg)
        print(colors.RED + 'Register fail' + colors.END)

    return render_template('signup.html', register='menu-active')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # TODO: 'username' -> form and variable name
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        error_msg = None

        user = User.query.filter_by(username=username).first()
        if user is None:
            error_msg = 'Wrong username'
        elif not check_password_hash(user.password, password):
            error_msg = 'Wrong password'

        if error_msg is None:
            endpoint = session.get('next', 'index')
            session.clear()
            session['user_id'] = user.id
            print(colors.GREEN + 'Login success' + colors.END)
            return redirect(url_for(endpoint))

        flash(error_msg)
        print(colors.RED + 'Login fail' + colors.END)

    return render_template('login.html', login='menu-active')

@bp.before_app_request
def load_logging_in_user_data():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

def force_login(endpoint):
    def deco(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            """if not logged in, redirect to login page"""
            if g.user is None:
                session['next'] = endpoint
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view
    return deco

