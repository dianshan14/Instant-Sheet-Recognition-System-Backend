from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'sheet_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(100), nullable=False)
    sheets = db.relationship('Sheet', backref='users')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Sheet(db.Model):
    __tablename__ = 'sheet'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    question_number = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('sheet_user.id'))
    questions = db.relationship('Question', backref='sheets')
    responses = db.relationship('Response', backref='sheets')

    # backref: users

    def __repr__(self):
        return '<Sheet {}>'.format(self.id)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.Text)
    # option_number = db.Column(db.Integer, nullable=False)
    option_title = db.Column(db.ARRAY(db.Text), nullable=False)

    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))

    # sheets

    def __repr__(self):
        return '<Question {}>'.format(self.id)

class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.Integer, primary_key=True)
    response_list = db.Column(db.ARRAY(db.Integer), nullable=False)

    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))

    # sheets

    def __repr__(self):
        return '<Answer {}>'.format(self.id)