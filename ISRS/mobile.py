from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, jsonify, Response
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

@bp.route('/check_login/')
def check_login():
    """
        check user login.
        Response: 0 is not logged-in, otherwise return user_id
    """
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return Response("login_success")
    else:
        return Response("login_fail")

@bp.route('/list/<user_id>')
def mobile_list_sheet(user_id):
    """
        Return user's sheets' id and title
    """
    ids = list()
    titles = list()
    
    user = User.query.filter_by(id=user_id).first()
    for sheet in user.sheets:
        ids.append(sheet.id)
        titles.append(sheet.title)

    return jsonify(ids=ids, titles=titles)
