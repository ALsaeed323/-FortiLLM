from flask import request, render_template, redirect, url_for, jsonify, session,make_response
from models.user_model import create_user, find_user_by_email, verify_password
import jwt
import datetime
import os


def register_controller():
    try:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        verify_human = request.form.get("verify_human")

        if not all([first_name, last_name, email, password, confirm_password]):
            return jsonify({"error": "All fields are required"}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        if verify_human != "on":
            return jsonify({"error": "Please verify you are human"}), 400

        if find_user_by_email(email):
            return jsonify({"error": "User already exists"}), 400

        full_name = f"{first_name} {last_name}"
        create_user(full_name, email, password)
        return redirect(url_for("home_page"))

    except Exception as e:
        print(f"Error in register_controller: {str(e)}")
        return jsonify({"error": "An unexpected error occurred during registration"}), 500


SECRET_KEY = os.getenv("SECRET_KEY")  # Make sure this is set in your environment

def login_controller():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        verify_human = request.form.get("verify_human")

        if not all([email, password]):
            return render_template("login.html", error="Email and password are required")
        if verify_human != "on":
            return render_template("login.html", error="Please verify you are human")

        user = find_user_by_email(email)
        if not user or not verify_password(user["password"], password):
            return render_template("login.html", error="Invalid credentials")

        # Save session
        session["full_name"] = user["name"]
        session["email"] = user["email"]

        # Generate token
        token = jwt.encode({
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        # Set token in secure HttpOnly cookie
        response = make_response(redirect(url_for("dashboard_page")))
        response.set_cookie("auth_token", token, httponly=True, secure=True, samesite='Lax')

        return response

    except Exception as e:
        print(f"Error in login_controller: {str(e)}")
        return render_template("login.html", error="An unexpected error occurred. Please try again."), 500
def logout_controller():
    try:
        session.clear()
        return redirect(url_for("home_page"))
    except Exception as e:
        print(f"Error in logout_controller: {str(e)}")
        return jsonify({"error": "An unexpected error occurred during logout"}), 500