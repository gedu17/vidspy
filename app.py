from flask import Flask, session, request, send_from_directory, render_template, redirect, Blueprint, g
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, PackageLoader
from controllers import *
from werkzeug.contrib.profiler import ProfilerMiddleware
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://vidspy:vidspy@localhost/vidspy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'bRbNHJf9cHe3T8XQqpW2R3Ya'
app.register_blueprint(settings_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(item_blueprint)
app.register_blueprint(items_blueprint)
app.register_blueprint(template_blueprint)
app.register_blueprint(system_messages_blueprint)
app.register_blueprint(real_item_blueprint)

# Globals
db = SQLAlchemy(app)
env = Environment(loader=PackageLoader('app', 'views'))

@app.before_request
def init():
	from consts import severity
	from classes.user import User
	user = User(request, session, db)
	sqldb = MySQLdb.connect(host='localhost', user='vidspy', passwd='vidspy', db='vidspy')

	g._env = env
	g._db = db.session
	g._user = user
	g._request = request
	g._session = session
	g._sqldb = sqldb

	if user.logged_in is not True and not is_unauthenticated_route():
		return redirect('/account/login')

def is_unauthenticated_route():
	if request.path[0:8] == '/public/':
		return True
	elif request.path[0:11] == '/item/view/':
		return True
	elif request.path[0:14] == '/account/login':
		return True
	else:
		return False


@app.route("/public/<path:path>")
def send_static(path):
	return send_from_directory('public', path)

if __name__ == "__main__":
	app.run()
