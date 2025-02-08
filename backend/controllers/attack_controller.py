import subprocess
import os
from flask import jsonify, request
import jwt
from functools import wraps
from models.attack_model import store_attack_result

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
        data = request.get_json()
        attack_type = data.get("attack_type", "injection")
        target = data.get("target", "LLM_API")

        # Define the FortiLLM Path
        FORTILLM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../fortillm/main.py"))

        # Run FortiLLM Attack using subprocess
        result = subprocess.run(
            ["python", FORTILLM_PATH],
            capture_output=True, text=True
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        # Store attack results
        #store_attack_result(attack_type, target, output, error)

        return jsonify({"output": output, "error": error})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
