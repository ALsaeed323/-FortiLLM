from flask import Blueprint
from controllers.fortillm_results_controller import receive_results_controller

fortillm_results_routes = Blueprint("fortillm_results_routes", __name__)

fortillm_results_routes.route("/api/fortillm_results", methods=["POST"])(receive_results_controller)
