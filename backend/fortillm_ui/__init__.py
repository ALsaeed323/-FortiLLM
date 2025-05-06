from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set secret key with fallback
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    print("Warning: SECRET_KEY not found in environment variables. Using default for development.")
    SECRET_KEY = "f7c5c9f8a38456b8575e6d6c"  # Use your original key as fallback
app.secret_key = SECRET_KEY

# Debug output to verify secret key
# print(f"Debug: Secret Key set to: {app.secret_key}")

# MongoDB configuration
# app.config['MONGO_URI'] = os.getenv("MONGO_URI", "mongodb://localhost:27017/market_db")
#mongodb+srv://alsaead2110679:${process.env.PASSWORD}@cluster0.vnvsld0.mongodb.net

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'  # You can change this to 'mongodb' if using MongoDB for sessions
Session(app)

# Initialize extensions
# mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login_page"  # Ensure this matches your route name
# login_manager.login_message_category = "info"

# Import and register routes
from routes import routes
# If routes is a Blueprint, register it like this:
# app.register_blueprint(routes)
