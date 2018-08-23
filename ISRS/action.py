import functools
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, jsonify, abort, Response
)

from ISRS.auth import force_login
from ISRS.model import db, User, Sheet, Question
from ISRS.color import colors

bp = Blueprint('action', __name__, url_prefix='/action')

@bp.route('/gen/', methods=['OPTIONS'])
def gen_option():
    res = Response("OK")
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return res

@bp.route('/gen/', methods=('GET', 'POST'), provide_automatic_options=False)
@force_login('action.generate_sheet')
def generate_sheet():
    """
        Get data of generated sheet
    """
    if request.method == 'POST':
        new_sheet = request.get_json()

        user = User.query.filter_by(id=g.user.id).first()
        sheet = Sheet(sheet_type=new_sheet['sheet_type'],
                      title=new_sheet['sheet_title'],
                      question_number=new_sheet['total_ques_num'],
                      option_number=new_sheet['total_opt_num'],
                      footer=new_sheet['sheet_footer'],
                      users=user)
        for question in new_sheet['ques_set']:
            Question(question_order=question['prob_num'],
                     question_title=question['problem'],
                     option_title=question['options'],
                     sheets=sheet)
        db.session.add(sheet)
        db.session.commit()

        res = redirect(url_for('action.list_sheet'))
        res.headers['Access-Control-Allow-Origin'] = '*'

        return res
        
    # TODO: store JSON data into sheet table
    # return redirect(url_for('action.list_sheet'))

    return render_template('template.html')

@bp.route('/edit/<sheet_id>/', methods=['OPTIONS'])
def edit_option():
    res = Response("OK")
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return res

@bp.route('/edit/<sheet_id>/', methods=('GET', 'POST'), provide_automatic_options=False)
@force_login('action.update_sheet')
def update_sheet(sheet_id):
    """
        Get data of generated sheet
    """
    if request.method == 'POST':
        new_sheet = request.get_json()

        sheet = Sheet.query.filter_by(id=sheet_id).first()
        sheet.sheet_type=new_sheet['sheet_type']
        sheet.title=new_sheet['sheet_title'],
        sheet.question_number=int(new_sheet['total_ques_num']),
        sheet.footer=new_sheet['sheet_footer'],

        # consider amount of questions!
        for old, new in zip(sheet.questions, new_sheet): # update
            old.question_order = new['prob_num']
            old.question_title = new['problem']
            old.option_title = new['options']

        old_length = len(sheet.questions)
        new_length = len(new_sheet['ques_set'])

        if old_length > new_length: # reduce
            reduce_number = old_length - new_length
            for i in range(new_length, new_length + reduce_number):
                db.session.delete(sheet.questions[i])
        elif old_length < new_length: # generate
            generate_number = new_length - old_length
            for i in range(old_length, old_length + generate_number):
                question = new_sheet['ques_set'][i]
                Question(question_order=question['prob_num'],
                         question_title=question['problem'],
                         option_title=question['options'],
                         sheets=sheet)

        db.session.add(sheet)
        db.session.commit()

        res = redirect(url_for('action.list_sheet'))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
        
    return render_template('edit.html')

@bp.route('/edit_json/<sheet_id>/', methods=('GET',))
@force_login('action.update_sheet_json')
def update_sheet_json(sheet_id):
    sheet = Sheet.query.filter_by(id=sheet_id).first()
    res = jsonify(
        sheet_title=sheet.title,
        sheet_footer=sheet.footer,
        sheet_type=sheet.sheet_type,
        total_ques_num=sheet.question_number,
        total_opt_num=sheet.option_number,
        ques_set=[
            {
                "prob_num": i + 1,
                "problem": sheet.questions[i].question_title,
                "options" : [
                    {
                        "opt_num": j + 1,
                        "description": option
                    } for j, option in enumerate(sheet.questions[i].option_title)
                ]
            } for i in range(len(sheet.questions))
        ]
    )
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@bp.route('/list/', methods=('GET',))
@force_login('action.list_sheet')
def list_sheet():
    """
        List sheet which belong to logged-in user
    """
    # TODO: Return all sheet of logged-in user
    # TODO
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

    res = jsonify(sheet_ids=sheet_ids,
                  sheet_titles=sheet_titles
                 )
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@bp.route('/visualize/<sheet_id>/', methods=('GET',))
@force_login('action.visualize_sheet')
def visualize_sheet(sheet_id):
    """
        Visualize specific sheet
    """

    # TODO : check 'sheet_id' whether belong to current logged-in user
    # return render_template('visualize_sheet.html')
    
    return '<h1 style="text-align: center;">Visualize' + sheet_id + '</h1>'

@bp.route('/visualize_json/<sheet_id>/', methods=('GET',))
@force_login('action.visualize_sheet_json')
def visualize_sheet_json(sheet_id):
    """ JSON response about sheet of specific user """
    sheet = Sheet.query.filter_by(id=sheet_id).first()
    
    # No this sheet id
    if sheet is None:
        abort(404)

    if g.user.id == sheet.user_id:
        question_titles = list()
        response_conclude = list()

        # if everything is empty ?

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

        res = jsonify(title=sheet.title,
                      question_title=question_titles,
                      response_conclude=response_conclude
                     )
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    
    # sheet does not belong to this user
    abort(401)

@bp.route('/about/', methods=('GET',))
def about():
    return render_template('about.html', about='menu-active')

@bp.route('/admin')
def list_user():
    users = User.query.all()
    data = dict(username=[user.username for user in users], 
                password=[user.password for user in users])
    return jsonify(data)
