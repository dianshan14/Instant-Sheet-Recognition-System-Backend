import functools
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g
)

from ISRS.auth import force_login
from ISRS.model import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/list_user/')
@force_login('admin.list_user')
@check_admin
def list_user():
    """
    List sheet which belong to logged-in user
    """
    
    # TODO: Return all sheet of logged-in user
    return '<h1 style="text-align: center;">List Sheet</h1>'

@bp.route('/list_sheet/')
@force_login('admin.list_sheet')
@check_admin
def list_sheet():
    pass


def check_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.username == 'admin':
            return view(**kwargs)
        return redirect(url_for('index'))
    return wrapped_view