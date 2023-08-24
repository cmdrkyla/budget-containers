from flask import Blueprint, jsonify, request

from auth.auth import Auth
from auth.route import secure_route
from functions import string_to_class


class Blueprint_Auth():
    blueprint = Blueprint("blueprint_auth", __name__)

    # Login
    @blueprint.route("/api/auth/login", methods=["POST"])
    def login():
        return Auth.login()
    
    # Logout
    @blueprint.route("/api/auth/logout", methods=["GET"])
    def logout():
        return Auth.logout()
    
    # Is Authenticated
    @blueprint.route("/api/auth/is_authenticated", methods=["GET"])
    def is_authenticated():
        return jsonify({"is_authenticated": Auth.is_authenticated()})


class Blueprint_Models():
    blueprint = Blueprint("blueprint_models", __name__)


    # Crudl based routing
    # Create
    @blueprint.route("/api/<model_name>/create", methods=['POST'])
    @secure_route
    def route_create(model_name:str):
        model = string_to_class(model_name)
        return str(model.create(request.form))


    # Read
    @blueprint.route("/api/<string:model_name>/read/<int:id>", methods=['GET'])
    @secure_route
    def route_read(model_name:str, id:int):
        model = string_to_class(model_name)
        return str(model.read(id))


    # Update
    @blueprint.route("/api/<model_name>/update/<int:id>", methods=['PUT'])
    @secure_route
    def route_update(self, model_name:str, id:int):
        model = self.string_to_class(model_name)
        return model.update(id)


    # Delete
    @blueprint.route("/api/<model_name>/delete/<int:id>", methods=['DELETE'])
    @secure_route
    def route_delete(self, model_name:str, id:int):
        model = self.string_to_class(model_name)
        return model.delete(id)


    # List
    @blueprint.route("/api/<model_name>/list", methods=['GET'])
    @secure_route
    def route_list(self, model_name:str):
        model = self.string_to_class(model_name)
        return model.list()