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

### Connect to a local DB called `fighters`
### and insert an admin user
connection = Connection()
fighterCollection = connection['fighters'].fighters
password = bcrypt.generate_password_hash('meo123')
admin = {'name': u'admin', 'password': password}
fighterCollection.insert(admin)

@db.register
class Fighter(Document):
	__collection__ = 'fighters'
	structure = {
		'name': unicode,
		'password': unicode,
	}
	required_fields = ['name', 'password']
	use_dot_notation = True

# config is a dictionary used by flask-wtf 
app.config['SECRET_KEY'] = '{E]\x1eo\xa3\x04w\xe2\x1b\xf7|\x97\x93N8\x7f\xa4\xf0\xe5\n\xa7\xfc\x02' 

class NameForm(Form):
	name = StringField('Name:', validators=[Required()])
	submit = SubmitField('Submit')


class LoginForm(Form):
	username = TextField('username', validators=[Required()])
	password = PasswordField('password', validators=[Required()])

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
	form = LoginForm(request.form)

	if request.method == 'POST':
		if form.validate_on_submit():
			print 'in here yo'
			fighter = db.Fighter()
			fighter.name = request.form['username']
			password = request.form['password']
			fighter.password = bcrypt.generate_password_hash(password)
			# fighterCollection.insert(fighter)
			session['username'] = fighter.name
			session['logged_in'] = True
			print "LOGGED IN AS ", session['username']
			return redirect(url_for('home'))
		else:
			error = 'What'

	return render_template('login.html', error=error, form=form)


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