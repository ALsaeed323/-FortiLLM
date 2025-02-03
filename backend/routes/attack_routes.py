from flask import Blueprint
from controllers.attack_controller import run_attack_controller

attack_routes = Blueprint("attack_routes", __name__)

attack_routes.route("/api/run_attack", methods=["POST"])(run_attack_controller)
