from flask import abort, Blueprint, jsonify, render_template
from sys import modules

import app
from auth.auth import Auth
from auth.route import secure_route
from controllers.activity import ActivityController
from controllers.container import ContainerController
from controllers.period import PeriodController
from controllers.user import UserController

class Blueprint_Auth():
    blueprint = Blueprint("blueprint_auth", __name__)

    # Login
    @blueprint.route("/api/auth/login", methods=["POST"])
    def login() -> any:
        return Auth.login()
    
    # Logout
    @blueprint.route("/api/auth/logout", methods=["GET"])
    def logout() -> any:
        return Auth.logout()
    
    # Is Authenticated
    @blueprint.route("/api/auth/is_authenticated", methods=["GET"])
    def is_authenticated() -> any:
        return jsonify({"is_authenticated": Auth.is_authenticated()})


# Crudl model based routing
class Blueprint_Models():
    blueprint = Blueprint("blueprint_models", __name__)

    # Create
    @blueprint.route("/api/<model_name>/create", methods=['POST'])
    @secure_route
    def route_create(model_name:str) -> any:
        model = string_to_class(model_name)
        record = model.create()
        if record:
            return record
        else:
            abort(500)


    # Read
    @blueprint.route("/api/<string:model_name>/read/<int:id>", methods=['GET'])
    @secure_route
    def route_read(model_name:str, id:int) -> any:
        model = string_to_class(model_name)
        record = model.read(id)
        if record:
            return record
        else:
            abort(500)


    # Update
    @blueprint.route("/api/<model_name>/update/<int:id>", methods=['PUT'])
    @secure_route
    def route_update(model_name:str, id:int) -> any:
        model = string_to_class(model_name)
        record = model.update(id)
        if record:
            return record
        else:
            abort(500)


    # Delete
    @blueprint.route("/api/<model_name>/delete/<int:id>", methods=['DELETE'])
    @secure_route
    def route_delete(model_name:str, id:int) -> any:
        model = string_to_class(model_name)
        record = model.delete(id)
        if record:
            return record
        else:
            abort(500)


    # List
    @blueprint.route("/api/<model_name>/list", methods=['GET'])
    @secure_route
    def route_list(model_name:str) -> any:
        model = string_to_class(model_name)
        records = model.list()
        return records


class Blueprint_Frontend():
    blueprint = Blueprint("blueprint_frontend", __name__)

    # Login
    @blueprint.route("/login")
    def login() -> any:
        return render_template("login.html")

    # Home
    @blueprint.route("/")
    def home() -> any:
        return render_template("home.html")

    # Activities
    @blueprint.route("/activities")
    def activities() -> any:
        return render_template("activities.html")

    # Containers
    @blueprint.route("/containers")
    def containers() -> any:
        return render_template("containers.html")

    # Periods
    @blueprint.route("/periods")
    def periods() -> any:
        return render_template("periods.html")

    # User
    @blueprint.route("/user")
    def user() -> any:
        return render_template("user.html")
    

# String to class object (for routing to correct module)
# TODO: Should I keep this or hardcode the routes in....
def string_to_class(class_string:str) -> object:
    # Turn snake_case to HeadedCamelCase first 
    class_pieces = class_string.split("_")
    model_name = "".join(piece.title() for piece in class_pieces)
    controller_name = model_name + "Controller"
    try:
        class_object = getattr(modules[__name__], controller_name)
        return class_object
    except AttributeError:
        app.app.logger.debug(f"Invalid module or controller: class_string={class_string}")
        return None