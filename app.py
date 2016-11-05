from flask import Flask, session, request, send_from_directory, render_template, redirect, Blueprint, g
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, PackageLoader
from controllers import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://vidspy:vidspy@localhost/vidspy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.secret_key = 'bRbNHJf9cHe3T8XQqpW2R3Ya'
app.register_blueprint(settings_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(item_blueprint)
app.register_blueprint(items_blueprint)
app.register_blueprint(template_blueprint)
app.register_blueprint(system_messages_blueprint)

# Globals
db = SQLAlchemy(app)
env = Environment(loader=PackageLoader('app', 'views'))

@app.before_request
def init():
	from consts import severity
	from classes.user import User
	user = User(request, session, db)

	g._env = env
	g._db = db.session
	g._user = user
	g._request = request

	if user.logged_in is not True and request.path[0:8] != '/public/':
		return login()
	


@app.route('/login', methods=['GET', 'POST'])
def login():
	from models.user import User

	if g._user.logged_in:
		return redirect('/')

	if request.method == 'GET':
		template = env.get_template('user_list.html')
		users = db.session.query(User).all()
		return template.render(users=users, user=g._user)
	elif request.method == 'POST':
		id = request.json['id']
		user = db.session.query(User).filter(User.id == id).first()
		if user is not None:
			session['user_id'] = id
			return 'OK'
	return 'Bad Request', 400

@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return redirect('/login')

@app.route("/public/<path:path>")
def send_static(path):
	return send_from_directory('public', path)




#TODO: remove when running from wsgi
if __name__ == "__main__":
	app.run()

