from flask import Flask
from flask_restplus import reqparse,Resource, Api
api = Api()



@api.route('/register')
class Register(Resource):
    response = {
        200:'OK',
        400:'Bad Input',
        404:"Forbidden"
    }
    @api.doc(response)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='first name is required.', required=True)
        parser.add_argument('last_name', type=str, help='last name is required.', required=True)
        parser.add_argument('email', type=str, help='email is required.', required=True)
        parser.add_argument('password', type=str, help='password is required', required=True)
        requested_data = parser.parse_args(strict=True)
        success = User.register(requested_data)  # create the new user
        if success:
              # store the user in the database
            msg = 'user has been created'  # return message and ok status code back to client
            status = 200
        else:
            msg = 'error in entering new user into the databse'
            status = 400
        return msg,status





# # from flask_restful import Resource,reqparse
# from flask_bcrypt import Bcrypt
# from flask import jsonify, request
# from flask_jwt_extended import (
#     JWTManager, jwt_required, create_access_token,
#     get_jwt_identity
# )
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import exc
# from app.resources.models import(
#     User, PermissionEntries,PermissionGroupMeta,
#     PermissionMembership,Fish,Event
# )


# class Login(Resource):
#     # Provide a method to create access tokens. The create_access_token()
#     # function is used to actually generate the token, and you can return
#     # it to the caller however you choose.
#     #@app.route('/login', methods=['POST'])
#     def post(self):
#         if not request.is_json:
#             return jsonify({"msg": "Missing JSON in request"}), 400

#         email = request.json.get('email', None)
#         password = request.json.get('password', None)
#         if not email or not password:
#             return jsonify({"msg": "Invalid parameters"}), 400

#         user = db.session.query(User).filter_by(email=email).first()

#         if not user or not Bcrypt.check_password_hash(user.password, password):
#             return jsonify({"msg": "Bad username or password"}), 401

#         # Identity can be any data that is json serializable
#         access_token = create_access_token(identity=user.id)
#         return jsonify(access_token=access_token), 200

# class Register(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('email', type=str, help='email is required', required=True)
#         request_data = parser.parse_args(strict=True)
#         user = User.get_user_by_email(request_data['email'])
#         if not user:
#             msg = 'error in deleting user'
#             status = 400
#             return msg, status
#         status = 200
#         return user, status

#     # CRUD-Create
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('first_name', type=str, help='first name is required.', required=True)
#         parser.add_argument('last_name', type=str, help='last name is required.', required=True)
#         parser.add_argument('email', type=str, help='email is required.', required=True)
#         parser.add_argument('password', type=str, help='password is required', required=True)
#         requested_data = parser.parse_args(strict=True)
#         success = User.register(requested_data)  # create the new user
#         if success:
#               # store the user in the database
#             msg = 'user has been created'  # return message and ok status code back to client
#             status = 200
#         else:
#             msg = 'error in entering new user into the databse'
#             status = 400
#         return msg,status

#     # CRUD-Delete
#     def delete(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('email', type=str, help='email is required', required=True)
#         request_data = parser.parse_args(strict=True)
#         success = User.delete_user(request_data['email'])
#         if success:
#             msg = 'User has been deleted'
#             status = 200
#         else:
#             msg = 'error in deleting user'
#             status = 400

#         return msg,status


#     # Protect a view with jwt_required, which requires a valid access token
#     # in the request to access.
# class Protected(Resource):
#     # @app.route('/', methods=['GET'])
#     @jwt_required
#     def get(self):
#         # Access the identity of the current user with get_jwt_identity
#         current_user = get_jwt_identity()
#         return jsonify(logged_in_as=current_user), 200

# class Index(Resource):
#     def get(self):
#         return "hello world"