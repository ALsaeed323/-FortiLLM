from flask import Blueprint
from controllers.results_controller import get_results_controller

results_routes = Blueprint("results_routes", __name__)

results_routes.route("/api/get_results", methods=["GET"])(get_results_controller)
