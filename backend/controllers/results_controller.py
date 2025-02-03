from flask import jsonify
from models.attack_model import get_attack_results

def get_results_controller():
    """Fetch stored attack results from MongoDB."""
    try:
        results = get_attack_results()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
