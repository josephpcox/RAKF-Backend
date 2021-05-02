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
