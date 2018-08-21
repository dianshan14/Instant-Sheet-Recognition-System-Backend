from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, jsonify, Response, current_app
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from ISRS.auth import force_login
from ISRS.model import db, User
from ISRS.color import colors

import os

bp = Blueprint('mobile', __name__, url_prefix='/mobile')

@bp.route('/recognition/', methods=['POST'])
def upload_photo():
    """
        upload photo from mobile phone and recognize this photo
    """
    print(colors.GREEN + '----- Mobile Upload file -----' + colors.END)
    print(request.files) # many file

    if 'file' not in request.files:
        print(colors.RED + 'No file' + colors.END)
        return Response('Fail')

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        print(colors.RED + 'No selected file' + colors.END)
        return Response('Fail')
    
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(colors.BLUE + 'File saved to '
              + os.path.join(current_app.config['UPLOAD_FOLDER'], filename) + colors.END)
        return Response('OK')

    return Response('Fail')

def allowed_file(filename):
    """
        Check filename allowed.
        rsplit(seprator, max) : return list with length = max+1
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/check_login/', methods=['POST'])
def check_login():
    """
        check user login.
        Response: 0 is not logged-in, otherwise return user_id
    """
    print(colors.GREEN + '----- Mobile check login -----' + colors.END)
    username = request.form['username']
    password = request.form['password']
    print(colors.BLUE + 'username: {}'.format(username) + colors.END)
    print(colors.BLUE + 'password: {}'.format(password) + colors.END)

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        print(colors.RED + 'Login fail!' + colors.END)
        return Response("login_fail")
    else:
        print(colors.BLUE + 'Login success!' + colors.END)
        return Response("login_success")

@bp.route('/list/<user_id>')
def mobile_list_sheet(user_id):
    """
        Return user's sheets' id and title
    """
    print(colors.GREEN + '----- Mobile list -----' + colors.END)
    print('user id ', user_id)
    ids = list()
    titles = list()
    
    user = User.query.filter_by(id=user_id).first()
    for sheet in user.sheets:
        ids.append(sheet.id)
        titles.append(sheet.title)

    return jsonify(ids=ids, titles=titles)
