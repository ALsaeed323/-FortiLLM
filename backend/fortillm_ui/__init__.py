from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb://localhost:27017/market_db' 
# app.config['SECRET_KEY'] = 'f7c5c9f8a38456b8575e6d6c'

# mongo = PyMongo(app)  
# bcrypt = Bcrypt(app) 
# login_manager = LoginManager(app) 
# login_manager.login_view = "login_page"
# login_manager.login_message_category = "info"

from fortillm_ui import routes
