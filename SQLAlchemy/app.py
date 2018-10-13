# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80),unique = True)
	email = db.Column(db.String(120),unique=True)

	def __init__(self,username,email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # post = db.relationship('Post')
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


# registrations = db.Table('registrations',
#                     db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
#                     db.Column('class_id', db.Integer, db.ForeignKey('classes.id')))

class Registration(db.Model):
    '''关联表'''
    __tablename__ = 'registrations'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    _class = db.relationship('Registration', foreign_keys=[Registration.student_id],
                             backref=db.backref('student', lazy="joined"), lazy="dynamic")
    def __repr__(self):
        return '<Student: %r>' %self.name
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship('Registration', foreign_keys=[Registration.class_id],
                               backref=db.backref('_class', lazy="joined"), lazy="dynamic")
    name = db.Column(db.String(64))
    def __repr__(self):
        return '<Class: %r>' %self.name

# if __name__ == '__main__':
#     db.drop_all()
#     db.create_all()
# 	python = Category('Python')
# 	post = Post('Hello Python','I love python',python)

# 	db.session.add(python)
# 	# db.session.add(post)
# 	db.session.commit()