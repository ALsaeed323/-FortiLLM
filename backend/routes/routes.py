from fortillm_ui import app
from flask import render_template,session, redirect, url_for
from controllers.auth_controller import register_controller, login_controller, logout_controller
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
    if "email" not in session:
        return redirect(url_for("login_page"))
    
    full_name = session.get("name")
    return render_template('dashboard.html', full_name=full_name)

app.route("/register", methods=["POST"])(register_controller)
app.route("/login", methods=["POST"])(login_controller)