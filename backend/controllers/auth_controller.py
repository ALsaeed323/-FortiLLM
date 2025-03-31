from flask import request, render_template, redirect, url_for, jsonify, session
from models.user_model import create_user, find_user_by_email, verify_password

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

        session["full_name"] = user["name"]
        session["email"] = user["email"]
        return redirect(url_for("dashboard_page"))

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