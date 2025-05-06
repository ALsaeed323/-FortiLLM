from flask import jsonify, session, request
from models.user_model import get_all_users, create_user, delete_user_by_email, update_user

def get_users_controller():
    """Fetch all users from MongoDB."""
    try:
        users = get_all_users()
        session["users"] = users  
        if not users:
            return jsonify({"message": "No users found"}), 404
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_user_controller():
    """Create a new user in MongoDB."""
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not all([name, email, password]):
            return jsonify({"error": "Name, email, and password are required."}), 400

        # Create the user
        create_user(name, email, password)
        return jsonify({"message": "User created successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user_controller():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        deleted = delete_user_by_email(email)
        if deleted:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_user_controller():
    """Update an existing user in MongoDB."""
    try:
        data = request.get_json()
        email = data.get("email")
        new_name = data.get("name")
        new_email = data.get("new_email")
        password = data.get("password")

        # Validate input
        if not email:
            return jsonify({"error": "Email is required"}), 400
        if not any([new_name, new_email, password]):
            return jsonify({"error": "At least one field (name, new_email, or password) must be provided"}), 400

        # Update the user
        updated = update_user(email, new_name=new_name, new_email=new_email, password=password)
        if updated:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500