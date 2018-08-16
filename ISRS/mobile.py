from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g
)

from ISRS.auth import force_login
from ISRS.model import db, User

bp = Blueprint('mobile', __name__, url_prefix='/mobile')

@bp.route('/recognition')
def upload_photo():
    """
        upload photo from mobile phone and recognize this photo
    """
    
    pass

@bp.route('/check_login/<username>')
def check_login(username):
    """
        check user login.
        Response: True or False
    """
    user = User.query.filter_by(username=username).first()
    if user:
        return "True"
    else:
        return "False"
