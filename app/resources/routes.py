from flask import Flask
from flask_restplus import reqparse,Resource, Api
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.resources.models import(
    User, 
    PermissionMembership, 
    PermissionGroupMeta, 
    PermissionEntries,
    Fish,
    Event
)

api = Api()



@api.route('/register')
class Register(Resource):
    response = {
        200:'OK',
        400:'Bad Input',
        404:'Forbidden',
        500:'server error'
    }
    parser = api.parser()
    parser.add_argument('first_name', type=str, help='first name is required.', required=True)
    parser.add_argument('last_name', type=str, help='last name is required.', required=True)
    parser.add_argument('email', type=str, help='email is required.', required=True)
    parser.add_argument('password', type=str, help='password is required', required=True)

    @api.doc(response)
    @api.expect(parser)
    def post(self):
        try:
            requested_data = self.parser.parse_args(strict=True)
            success = User.register(requested_data)  # create the new user
            if success:
                # store the user in the database
                msg = 'user has been created'  # return message and ok status code back to client
                status = 200
            else:
                api.abort(400)
        except Exception as e:
            return {'msg':str(e)},500
        
        return msg,status

@api.route('/login')
class Login(Resource):
    response = {
        200:'OK',
        400:'Bad Input',
        404:'Forbidden',
        500:'server error'
    }
    parser = api.parser()
    parser.add_argument('email', type=str, help='email is required.', required=True)
    parser.add_argument('password', type=str, help='password is required', required=True)

    @api.doc(response)
    @api.expect(parser)
    def post(self):
        try:
            requested_data = self.parser.parse_args(strict=True)
            token = User.userLogin(requested_data)
            if token is not None:
                return {'token':token,'status':200}
            else:
                api.abort(404)
        except Exception as e:
            return {'msg':str(e)},500


@api.route('/admin/get_users')
class AdminManageUsers(Resource):
    response = {
        200:'OK',
        204:'No Content',
        400:'Bad Input',
        404:'Forbidden',
        500:'server error'
    }
    @jwt_required()
    @api.doc(response)
    def get(self):
        try:
            user_id=get_jwt_identity()
            result = User.get_users()
            if not result:
                api.abort(204)
            else:
                return result, 200
        except Exception as e:
            return {'msg':str(e)},500







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