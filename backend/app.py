from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urllib.parse.quote('your-secret-key')

# Register Blueprints (Routes)
app.register_blueprint(auth_routes)
app.register_blueprint(attack_routes)
app.register_blueprint(results_routes)
app.register_blueprint(fortillm_results_routes)  

if __name__ == "__main__":
    app.run(debug=True)
