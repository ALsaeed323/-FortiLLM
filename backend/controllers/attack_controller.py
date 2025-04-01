import subprocess
import os
import jwt
from functools import wraps
from models.attack_model import store_attack_result
from flask import jsonify, request, render_template

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            jwt.decode(token.split("Bearer ")[1], SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated

def run_attack_controller():
    """Handles running an attack and storing the result."""
    try:
        attack_type = request.form.get("intention", "injection")
        target = request.form.get("target_app", "LLM_API")
        print(f"Debug: Attack Type: {attack_type}, Target: {target}")

        FORTILLM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../fortillm/main.py"))
        print(f"Debug: FORTILLM_PATH: {FORTILLM_PATH}")
        result = subprocess.run(
            ["python", FORTILLM_PATH]
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        return render_template('attack.html',
                             framework=target,
                             response=output if output else error)
    except Exception as e:
        return render_template('attack.html', error=str(e))