from fortillm_ui import app
from flask import render_template
# , redirect, url_for, flash, request
# from fortillm_ui.models import Item, User
# from fortillm_ui.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
# from fortillm_ui import db 
# from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/run_attack')
def run_attack_page():
    return render_template('attack.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')