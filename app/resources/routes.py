from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask import jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from app.resources.models import User


class Login(Resource):
    # Provide a method to create access tokens. The create_access_token()
    # function is used to actually generate the token, and you can return
    # it to the caller however you choose.
    #@app.route('/login', methods=['POST'])
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email or not password:
            return jsonify({"msg": "Invalid parameters"}), 400

        user = db.session.query(User).filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"msg": "Bad username or password"}), 401

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

class Register(Resource):
    # @app.route('/register', methods=['POST'])
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        user = User(
            email=request.json.get('email', None),
            # decode the hash to prevent is encoded twice
            password=bcrypt.generate_password_hash(request.json.get('password', None)).decode('utf8'),
            first_name=request.json.get('first_name', None),
            last_name=request.json.get('last_name', None)
        )

        try:

            db.session.add(user)
            db.session.commit()

            return jsonify({"msg": "Registered successfully"}), 201

        except exc.IntegrityError:
            return jsonify({"msg": "A user is already registered with that email address"}), 409


    # Protect a view with jwt_required, which requires a valid access token
    # in the request to access.
class Protected(Resource):
    # @app.route('/', methods=['GET'])
    @jwt_required
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200

class Index(Resource):
    def get(self):
        return "hellow world"