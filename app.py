from flask import Flask 
from flask import render_template
from functools import wraps
from flask import request, url_for, redirect, session, g, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Required
from mongokit import Connection, Document
import os

### DB configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

### Our applications name:
app = Flask(__name__)

### Connect to a local DB called `fighters`
connection = Connection()
testCollection = connection['fighters'].fighters
user = {'name': u'admin', 'email': u'admin@localhost'}
# testCollection.insert(user)


# for development
user = 'sammy'
password = '123qwe'

app.config['SECRET_KEY'] = 	'{E]\x1eo\xa3\x04w\xe2\x1b\xf7|\x97\x93N8\x7f\xa4\xf0\xe5\n\xa7\xfc\x02' # .config is a dictionary used by flask-wtf 

class NameForm(Form):
	name = StringField('Name:', validators=[Required()])
	submit = SubmitField('Submit')

# login_required decorator to ensure a user is logged in
def login_required(function):
	@wraps(function)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return function(*args, **kwargs)
		else:
			return redirect (url_for('login'))
	return wrap


@app.route('/', methods=["GET", "POST"])
def login():
	name = None
	error = ''

	if request.method == "POST":
		if request.form['user'] == user and request.form['password'] == password:
			session['username'] = request.form['user']
			session['logged_in'] = True
			flash('You were successfully logged in')
			print session.items()
			print 'You are logged in as ' + session['username']
			return redirect (url_for('home'))
		else:
			error = "Invalid Credentials"

	return render_template('login.html', error=error)


@app.route('/home')
@login_required #decorator used to require a login for this view function
def home():
	return render_template('index.html', name=session.get('username'))


@app.route('/record')
@login_required
def record():
	return render_template('record.html', name=session.get('username'))


@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('logged_in', None)
	print session.items()
	print 'You are now logged out'
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True)