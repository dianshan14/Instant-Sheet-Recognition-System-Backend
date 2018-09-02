from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, jsonify, Response, current_app,send_from_directory
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from datetime import datetime, timedelta

from ISRS.auth import force_login
from ISRS.model import db, User, Sheet
from ISRS.model import Response as db_Response
from ISRS.color import colors
from ISRS.sheet_detect.detect_row import sheet_recognition_type_one
from ISRS.sheet_detect.hough import sheet_recognition_type_one_sam

import os

bp = Blueprint('mobile', __name__, url_prefix='/mobile')

@bp.route('/recognition/<username>/', methods=['POST'])
def upload_photo(username):
    """
        upload photo from mobile phone and recognize this photo
        args:
            username: For checking login!
    """
    print(colors.GREEN + '----- Mobile Upload file -----' + colors.END)
    print(request.files) # many file

    if 'file' not in request.files:
        print(colors.RED + 'No file' + colors.END)
        return Response('file_failed')

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        print(colors.RED + 'No selected file' + colors.END)
        return Response('file_failed')

    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        saved_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(saved_filename)
        sheet_id = int(filename.split('_')[0])
        print(colors.BLUE + 'File saved to '
              + saved_filename + ', sheet_id: ' + str(sheet_id) + colors.END)

        sheet = Sheet.query.filter_by(id=sheet_id).first()
        sheet_type = sheet.sheet_type

        # TODO : check whether answer is valid -> recognition_failed
        # OK TODO : os.path
        # TODO sheet_type 1 or 2,
        # OK TODO : login user
        sheet_answer_wei = sheet_recognition_type_one(saved_filename, sheet.question_number, sheet.option_number)
        #sheet_answer_wei = 1
        print(colors.BLUE + 'Wei answer: ', end='')
        print(sheet_answer_wei, end='')
        print(colors.END)
        sheet_answer_sam = sheet_recognition_type_one_sam(saved_filename, sheet.question_number, sheet.option_number)
        #sheet_answer_sam = 1
        print(colors.BLUE + 'Sam answer: ', end='')
        print(sheet_answer_sam, end='')
        print(colors.END)
        if not sheet_answer_wei or not sheet_answer_sam:
            print(colors.YELLOW + 'Recognition failed' + colors.END)
            return Response('recognition_failed')
        elif sheet_answer_wei != sheet_answer_sam:
            print(colors.YELLOW + 'Recognition failed' + colors.END)
            return Response('recognition_failed')
        else:
            print(colors.GREEN + 'Recognition successed' + colors.END)
            add_response_record(sheet_id, sheet_answer_wei)

        return Response('success') # recognition success

    print(colors.RED + 'File extension not allowed or file not exist' + colors.END)
    return Response('file_failed')

def allowed_file(filename):
    """
        Check filename allowed.
        rsplit(seprator, max) : return list with length = max+1
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/answer/', methods=['POST'])
def add_response():
    data = request.get_json()
    print(data)
    add_response_record(data['sheet_id'], data['answer_list'])
    return 'OK'

def add_response_record(sheet_id, answer_list):
    if sheet_id > 0 and answer_list:
        sheet = Sheet.query.filter_by(id=sheet_id).first()
        new_response = db_Response(response_list=answer_list,
                                   created_at=(datetime.utcnow()+timedelta(hours=8)).strftime('%Y/%m/%d %H:%M:%S'),
                                   sheets=sheet)
        db.session.add(new_response)
        db.session.commit()
        return True
    return False

@bp.route('/check_login/', methods=['POST'])
def check_login():
    """
        check user login.
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

@bp.route('/list/<username>/')
def mobile_list_sheet(username):
    """
        Return user's sheets' id and title
    """
    print(colors.GREEN + '----- Mobile list -----' + colors.END)
    print('username ', username)

    user = User.query.filter_by(username=username).first()
    ids = [sheet.id for sheet in user.sheets]
    titles = [sheet.title for sheet in user.sheets]

    return jsonify(ids=ids, titles=titles)

@bp.route('get_img', methods=['GET'])
def get_img():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    print(files)
    return render_template('browser.html', files=files)

@bp.route('/imgs/<filename>/')
def imgs(filename):
    return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)
