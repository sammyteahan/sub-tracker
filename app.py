from flask import Flask 
from flask import render_template
from functools import wraps
from flask import request, url_for, redirect, session, g, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired, Required
from flask.ext.mongokit import MongoKit
from mongokit import Connection, Document
from flask.ext.bcrypt import Bcrypt
import os

### DB configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

### Our applications name:
app = Flask(__name__)
bcrypt = Bcrypt(app)
db = MongoKit(app)

### Connect to a local DB called `fighters`,
### and insert an admin user
connection = Connection()
fighterCollection = connection['fighters'].fighters

@db.register
class Fighter(Document):
	__collection__ = 'fighters'
	structure = {
		'name': unicode,
		'password': unicode,
		'wins': int,
		'losses': int,
		'submissions': [
			{'name': unicode, 'count': int}
		]
	}
	required_fields = ['name', 'password']
	use_dot_notation = True

### This inserts a fighter into the db
# only run once though to avoid duplicates
# sam = Fighter()
# sam.name = 'sammy'
# sam.password = bcrypt.generate_password_hash('meo123')
# sam.win = 0
# sam.loss = 0
# sam.submissions.append({'name': 'armbar','count': 1})
# sam.submissions.append({'name': 'triangle','count': 1})
# sam.submissions.append({'name': 'baseball bat choke','count': 3})
# fighterCollection.insert(sam)

# config is a dictionary used by flask
app.config['SECRET_KEY'] = '{E]\x1eo\xa3\x04w\xe2\x1b\xf7|\x97\x93N8\x7f\xa4\xf0\xe5\n\xa7\xfc\x02' 

class NameForm(Form):
	name = StringField('Name:', validators=[Required()])
	submit = SubmitField('Submit')


class LoginForm(Form):
	username = TextField('username', validators=[Required()])
	password = PasswordField('password', validators=[Required()])


### Form for sweep or submit view
# class Sweep_or_submit_form(Form):


# login_required decorator to ensure a user is logged in
def login_required(function):
	@wraps(function)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return function(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrap

@app.route('/', methods=["GET", "POST"])
def login():
	name = None
	error = ''
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			user = fighterCollection.find_one({'name': request.form['username']}) # finds user
			print user['name']
			print user['password']
			if user is not None and bcrypt.check_password_hash(user['password'], request.form['password']):
				print 'user authenticated'
				session['username'] = user['name']
				session['logged_in'] = True
				return redirect(url_for('home'))
			else:
				print 'User not in DB'
		else:
			error = 'Invalid Form'
	return render_template('login.html', error=error, form=form)

#decorator used to require a login for this view function
@app.route('/home')
@login_required 
def home():
	return render_template('index.html', name=session.get('username'))


@app.route('/record')
@login_required
def record():
	return render_template('record.html', name=session.get('username'))


@app.route('/roll')
@login_required
def roll():
	return render_template('roll.html', name=session.get('username'))


@app.route('/stats')
@login_required
def stats():
	return render_template('stats.html', name=session.get('username'))


@app.route('/sweep-or-submit')
@login_required
def sweep_or_submit():
	return render_template('sweep-or-submit.html', name=session.get('username'))


@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('logged_in', None)
	print session.items()
	print 'You are now logged out'
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True)