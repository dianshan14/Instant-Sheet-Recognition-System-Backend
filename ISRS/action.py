import functools
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, jsonify, abort
)

from ISRS.auth import force_login
from ISRS.model import db, User, Sheet, Question, Response
from ISRS.color import colors

bp = Blueprint('action', __name__, url_prefix='/action')

@bp.route('/gen/', methods=('GET', 'POST'))
@force_login('action.generate_sheet')
def generate_sheet():
    """
        Get data of generated sheet
    """
    if request.method == 'POST':
        new_sheet = request.get_json()

        # if arg exist -> update
        # else gen
        user = User.query.filter_by(id=g.user.id).first()
        sheet = Sheet(sheet_type=new_sheet['sheet_type'],
                      title=new_sheet['sheet_title'],
                      question_number=int(new_sheet['total_ques_num']),
                      footer=new_sheet['sheet_footer'],
                      users=user)
        for question in new_sheet['ques_set']:
            Question(question_order=question['prob_num'],
                     question_title=question['problem'],
                     option_title=question['options'],
                     sheets=sheet)
        db.session.add(sheet)
        db.session.commit()

        return redirect(url_for('action.list_sheet'))
        
    # TODO: store JSON data into sheet table
    # return redirect(url_for('action.list_sheet'))

    return render_template('template.html')

@bp.route('/list/')
@force_login('action.list_sheet')
def list_sheet():
    """
        List sheet which belong to logged-in user
    """
    # TODO: Return all sheet of logged-in user
    # return render_template('list_sheet.html')

    return '<h1 style="text-align: center;">List Sheet</h1>'

@bp.route('/list_json/', methods=('GET',))
@force_login('action.list_sheet_json')
def list_sheet_json():
    """ JSON response about sheet of specific user """
    user = User.query.filter_by(id=g.user.id).first()
    sheets = user.sheets
    sheet_ids = list()
    sheet_titles = list()

    for sheet in sheets:
        sheet_ids.append(sheet.id)
        sheet_titles.append(sheet.title)

    return jsonify(sheet_ids=sheet_ids,
                   sheet_titles=sheet_titles
                   )


@bp.route('/visualize/<sheet_id>/', methods=('GET', 'POST'))
@force_login('action.visualize_sheet')
def visualize_sheet(sheet_id):
    """
        Visualize specific sheet
    """

    # TODO : check 'sheet_id' whether belong to current logged-in user
    # return render_template('visualize_sheet.html')
    
    return '<h1 style="text-align: center;">Visualize' + sheet_id + '</h1>'

@bp.route('/visualize_json/<sheet_id>/', methods=('GET', 'POST'))
@force_login('action.visualize_sheet_json')
def visualize_sheet_json(sheet_id):
    """ JSON response about sheet of specific user """
    sheet = Sheet.query.filter_by(id=sheet_id).first()
    
    # No this sheet id
    if sheet is None:
        abort(404)

    if g.user.id == sheet.user_id:
        question_titles = list()
        option_titles = list()
        response_conclude = list()

        # if everything is empty ?

        """
        for question in sheet.questions: # all questions belong to this sheet
            question_titles.append(question.question_title) # collect all question title
            option_titles.append(question.option_title) # collect all option title
            response_sum = dict()
            for num in range(1, len(question.option_title)+1):
                response_sum[str(num)] = 0 # spell specific question and its option '1', '2', '3',...
            response_conclude.append(response_sum) # order is question order

        # collect responses
        for response in sheet.responses:
            for i, choose in enumerate(response.response_list):
                response_conclude[i][str(choose)] += 1
        """

        for question in sheet.questions:
            question_titles.append(question.question_title)
            
            question_object = list()
            for option_title in question.option_title:
                option_object = dict()
                option_object['description'] = option_title
                option_object['value'] = 0
                question_object.append(option_object)
            response_conclude.append(question_object)

        for response in sheet.responses:
            for i, choose in enumerate(response.response_list):
                response_conclude[i][choose-1]['value'] += 1

        return jsonify(title=sheet.title,
                       question_title=question_titles,
                       response_conclude=response_conclude
                      )
    
    # sheet does not belong to this user
    abort(401)

@bp.route('/about')
def about():
    return render_template('about.html', about='menu-active')

@bp.route('/admin')
def list_user():
    users = User.query.all()
    data = dict()
    data['username'] = list()
    data['password'] = list()
    for user in users:
        data['username'].append(user.username)
        data['password'].append(user.password)
        print(user.username)
    return jsonify(data)
