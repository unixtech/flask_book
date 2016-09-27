"""
Testing Flask with Flask book
"""
import os
from flask import Flask, url_for, request, g, render_template, redirect, session, flash
from flask_wtf import Form
from flask_script import Manager, Shell
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

#Application initioalize
APP = Flask(__name__)
MANAGER = Manager(APP)
WTF_CSRF_ENABLED = True
APP.config['SECRET_KEY'] = 'hard to guest1'

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
APP.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(APP)

def make_shell_context():
    return dict(APP=APP, db=db, User=User, Role=Role)
MANAGER.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(APP, db)
MANAGER.add_command('db', MigrateCommand)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    name = StringField('Name', validators=[DataRequired() ])
    submit = SubmitField('Submit')

@APP.route('/', methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
            print(user)
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known', False))


if __name__ == '__main__':
    # APP.run(host="10.0.11.31", port=8000, debug=True)
    MANAGER.run()
