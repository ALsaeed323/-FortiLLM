from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_routes
from routes.attack_routes import attack_routes
from routes.results_routes import results_routes
from routes.fortillm_results_routes import fortillm_results_routes  # <-- Import FortiLLM Results Route

app = Flask(__name__)
CORS(app)

# Register Blueprints (Routes)
app.register_blueprint(auth_routes)
app.register_blueprint(attack_routes)
app.register_blueprint(results_routes)
app.register_blueprint(fortillm_results_routes)  

if __name__ == "__main__":
    app.run(debug=True)
