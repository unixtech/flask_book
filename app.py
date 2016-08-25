"""
Testing Flask with Flask book
"""
from flask import Flask, url_for, request, g, render_template, redirect, session, flash
from flask_wtf import Form
from flask_script import Manager
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

#Application initioalize
APP = Flask(__name__)
MANAGER = Manager(APP)
WTF_CSRF_ENABLED = True
APP.config['SECRET_KEY'] = 'hard to guest1'

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(APP)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), Unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    name = StringField('Name', validators=[DataRequired() ])
    submit = SubmitField('Submit')

@APP.route('/', methods=["GET", "POST"])
def index():
    name = None
    form = NameForm()
    if request.method == 'POST' and form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name to\t" + form.name.data)
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    # APP.run(host="10.0.11.31", port=8000, debug=True)
    MANAGER.run()
