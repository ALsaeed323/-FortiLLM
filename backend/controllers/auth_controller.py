import jwt
import datetime
import os
from flask import jsonify, request
from models.user_model import create_user, find_user_by_email, verify_password

SECRET_KEY = os.getenv("SECRET_KEY")

def signup_controller():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    if find_user_by_email(data["email"]):
        return jsonify({"error": "User already exists"}), 400

    create_user(data["email"], data["password"])
    return jsonify({"message": "User registered successfully!"}), 201

def login_controller():
    data = request.get_json()
    user = find_user_by_email(data["email"])

    if not user or not verify_password(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"email": user["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200

def logout_controller():
    return jsonify({"message": "Logged out successfully!"}), 200
