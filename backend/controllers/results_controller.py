from flask import jsonify,session
from models.attack_model import get_attack_results

def get_results_controller():
    """Fetch stored attack results from MongoDB."""
    try:
        results = get_attack_results()
        session["results"] = results # Store results in session for later use
        if not results:
            return jsonify({"message": "No results found"}), 404
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
