from fortillm_ui import app 
from flask import render_template, session, redirect, url_for
from controllers.auth_controller import register_controller, login_controller, logout_controller
from controllers.attack_controller import run_attack_controller, token_required
from controllers.fortillm_results_controller import receive_results_controller
from controllers.results_controller import get_results_controller
from controllers.admin_controller import get_users_controller , create_user_controller, delete_user_controller, update_user_controller

# Public Pages
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Auth-Protected Pages
@app.route('/run-attack', methods=['GET'])
@token_required
def run_attack_page():
    get_results_controller()
    if "email" not in session:
        return redirect(url_for("login_page"))
    results = session.get("results")
    return render_template('attack.html', results=results)

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard_page():
    get_results_controller()
    get_users_controller()
    if "email" not in session:
        return redirect(url_for("login_page"))
    full_name = session.get("full_name")
    email = session.get("email")
    results = session.get("results")
    users = session.get("users")
    return render_template('dashboard.html', full_name=full_name, results=results, email=email, users=users)

@app.route('/dashboard/users/create', methods=['POST'])
@token_required
def api_create_user():
    return create_user_controller()

@app.route('/dashboard/users/delete', methods=['POST'])
@token_required
def api_delete_user():
    return delete_user_controller()

@app.route('/dashboard/users/update', methods=['POST'])
@token_required
def api_update_user():
    return update_user_controller()

@app.route('/dashboard/api-key-management', methods=['GET'])
@token_required
def api_key_management():
    return render_template('api_key_management.html')

@app.route('/dashboard/attack-executions', methods=['GET'])
@token_required
def attack_executions():
    return render_template('attack_executions.html')

@app.route('/dashboard/system-alerts', methods=['GET'])
@token_required
def system_alerts():
    return render_template('system_alerts.html')

@app.route('/dashboard/compliance-reports', methods=['GET'])
@token_required
def compliance_reports():
    return render_template('compliance_reports.html')

@app.route('/dashboard/api_usage_monitoring', methods=['GET'])
@token_required
def api_usage_monitoring():
    return render_template('api_usage_monitoring.html')

@app.route('/dashboard/external-api-access', methods=['GET'])
@token_required
def external_api_access():
    return render_template('external_api_access.html')

# API Routes
app.route("/register", methods=["POST"])(register_controller)
app.route("/login", methods=["POST"])(login_controller)
app.route("/run-attack", methods=["POST"])(token_required(run_attack_controller))
app.route("/fortillm_results", methods=["POST"])(token_required(receive_results_controller))
app.route('/get_results', methods=['GET'])(token_required(get_results_controller))
app.route('/logout', methods=['GET'])(logout_controller)
