from flask import Blueprint
from controllers.auth_controller import signup_controller, login_controller, logout_controller

auth_routes = Blueprint("auth_routes", __name__)

auth_routes.route("/api/signup", methods=["POST"])(signup_controller)
auth_routes.route("/api/login", methods=["POST"])(login_controller)
auth_routes.route("/api/logout", methods=["POST"])(logout_controller)
