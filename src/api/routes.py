"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/user', methods=['GET'])
def getUsers():

    users = User.query.all()
    users_list = list(map(lambda x: x.serialize(), users))

    return jsonify(users_list), 200

@api.route('/token', methods=['POST'])
def create_token():

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()

    if user is None:
        return jsonify({"msg": "Email or Password incorrect"}), 401
    #access_token = create_access_token(identity=user.id)
    access_token = create_access_token(identity=user.email)
    return jsonify({"access_token": access_token}), 200

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()
    #user = User.query.get(current_user_id)
    user = User.query.filter_by(email=current_user_id).first()
    
    return jsonify({"msg": "ok"}), 200