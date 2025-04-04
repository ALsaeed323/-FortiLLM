from fortillm_ui import app 
from flask import render_template, session, redirect, url_for
from controllers.auth_controller import register_controller, login_controller, logout_controller
from controllers.attack_controller import run_attack_controller, token_required
from controllers.fortillm_results_controller import receive_results_controller
from controllers.results_controller import get_results_controller

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

@app.route('/run-attack', methods=['GET'])
@token_required
def run_attack_page():
    get_results_controller()
    if "email" not in session:
        return redirect(url_for("login_page"))
    results = session.get("results")
    return render_template('attack.html', results=results)

@app.route('/dashboard')
@token_required
def dashboard_page():
    get_results_controller()
    if "email" not in session:
        return redirect(url_for("login_page"))
    full_name = session.get("full_name")
    email = session.get("email")
    results = session.get("results")
    print(f"Debug: Full name from session: {full_name}")
    return render_template('dashboard.html', full_name=full_name, results=results, email=email)

# Securing controller endpoints
app.route("/register", methods=["POST"])(register_controller)
app.route("/login", methods=["POST"])(login_controller)

# Wrap POST attack route with token requirement
app.route("/run-attack", methods=["POST"])(token_required(run_attack_controller))
app.route("/fortillm_results", methods=["POST"])(token_required(receive_results_controller))
app.route('/get_results', methods=['GET'])(token_required(get_results_controller))
app.route('/logout', methods=['GET'])(logout_controller)
