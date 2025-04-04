from flask import jsonify, request
from models.attack_model import store_fortillm_result

def receive_results_controller():
    """Receives attack results from FortiLLM and stores them in MongoDB."""
    try:
        data = request.get_json()
        print(f"Debug: Received data: {data}")
        if not data:
            print("Debug: No data received")
            return jsonify({"error": "No data received"}), 400
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        store_fortillm_result(data)  # Store FortiLLM results

        return jsonify({"message": "Attack results stored successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
