import jwt
import datetime

from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from models.user_model import create_user, find_user_by_email, verify_password
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def register_controller():
    # Get form data (not JSON)
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    verify_human = request.form.get("verify_human")

    # Basic validation
    if not all([first_name, last_name, email, password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if verify_human != "on":  # Checkbox sends "on" when checked
        return jsonify({"error": "Please verify you are human"}), 400

    # Check if user already exists
    if find_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    # Create user
    full_name = f"{first_name} {last_name}"
    create_user(full_name, email, password)
    # Redirect to home page after successful registration
    return redirect(url_for("home_page"))

def login_controller():
    # Get form data
    #print(request.form)
    email = request.form.get("email")
    password = request.form.get("password")
    verify_human = request.form.get("verify_human")


    # Basic validation
    if not all([email, password]):
        return render_template("login.html", error="Email and password are required")
    if verify_human != "on":
        return render_template("login.html", error="Please verify you are human")

    # Find user and verify password
    user = find_user_by_email(email)
    if not user or not verify_password(user["password"], password):
        return render_template("login.html", error="Invalid credentials")

    # Store token in session (or use a cookie)
    session["full_name"] = user["name"]
    session["email"] = user["email"]
    return redirect(url_for("dashboard_page"))

def logout_controller():
    return jsonify({"message": "Logged out successfully!"}), 200
