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
    answers = db.relationship('Answer', backref='sheets')

    # backref: users

    def __repr__(self):
        return '<Sheet {}>'.format(self.id)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.ARRAY(db.Text))

    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))
    options = db.relationship('Option', backref='questions')

    # sheets

    def __repr__(self):
        return '<Question {}>'.format(self.id)

class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.Integer, primary_key=True)
    option_number = db.Column(db.ARRAY(db.Integer), nullable=False)
    option_title = db.Column(db.ARRAY(db.Text), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return '<Option {}>'.format(self.id)

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.ARRAY(db.Integer), nullable=False)

    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))

    # sheets

    def __repr__(self):
        return '<Answer {}>'.format(self.id)