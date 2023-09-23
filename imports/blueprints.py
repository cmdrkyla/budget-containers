from flask import abort, Blueprint, jsonify, request

from auth.auth import Auth
from auth.route import secure_route
from imports.functions import string_to_class


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


# Crudl based routing
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
        if records:
            return records
        else:
            abort(500)