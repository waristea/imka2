# project/__init__.py

from flask import Flask, request

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from project.config import Config
from project import controllers
from flask_login import LoginManager

# config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# get current user
@login_manager.user_loader
def load_user(user_id):
    from project.models import User
    return User.query.get(int(user_id))

# routes
@app.route('/')
def index():
    return controllers.index()

@app.route('/signup', methods=['GET', 'POST'])
def register():
    return controllers.register()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return controllers.login()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return controllers.logout()

# IMKA yang dipakai
# Read open request(s)
@app.route('/request/<request_id>/photo', methods=['GET'])
def request_photo(request_id):
    return controllers.request_photo(request_id)

@app.route('/request/<request_id>/status', methods=['POST'])
def request_change_status(request_id):
    return controllers.request_change_status(request_id)

@app.route('/request/all', methods=['GET'])
def request_all():
    return controllers.request_all()

# API
# Create new open request
@app.route('/api/request', methods=['POST'])
def api_request_create():
    return controllers.api_request_create()

# Read open request(s)
@app.route('/api/request/<request_id>', methods=['GET', 'POST'])
def api_request_detail(request_id):
    if request.method=='GET':
        return controllers.api_request_detail(request_id)
    else: #request.method=='POST':
        return controllers.api_request_detail_change(request_id)
