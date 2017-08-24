from flask import request
from flask_restplus import abort, Resource, Namespace, fields
from app.models.user import User
from app.utils.utilities import validate_email


auth_api = Namespace(
    'auth', description='User authentication and registration')

USER = auth_api.model(
    'User',
    {
        'first_name': fields.String(
            required=True, description='User first name', example='fName'),
        'last_name': fields.String(
            required=True, description='User last name', example='lName'),
        'email': fields.String(
            required=True, description='User email', example='lname@test.com'),
        'password': fields.String(
            required=True, description='User password', example='123'),
    })


@auth_api.route('/register', endpoint='register')
class RegisterUser(Resource):
    ''' Class for User Registration '''
    @auth_api.response(201, {'message': 'User registered successfully'})
    @auth_api.response(401, {'message': 'Error while creating your account'})
    @auth_api.response(409, {'message': 'User already exists!'})
    @auth_api.response(500, {'message': 'Server Error. Couldn\'t complete request'})
    @auth_api.doc(model='User', body=USER)
    def post(self):
        ''' Method to handle POST request for User registration '''
        arguments = request.get_json(force=True)
        first_name, last_name, email = arguments.get(
            'first_name'), arguments.get('last_name'), arguments.get('email').lower()
        password, password_confirm = arguments.get(
            'password'), arguments.get('password_confirm')

        if not validate_email(email):
            return abort(401, message='email address is invalid.')
        if password != password_confirm:
            return abort(401, message='Password doesn\'t match confirmation')
        if not first_name or not last_name:
            return abort(400, 'First Name AND Last Name should be provided')

        user = User(email=email, first_name=first_name,
                    last_name=last_name, password=password)

        try:
            confirm = user.save_user()
            if confirm:
                response = {'message': 'User registration successful.'}
                return response, 201
            else:
                response = {'message': 'User already Exists!. Login'}
                return response, 409
        except Exception as e:
            abort(400, 'Error while creating your account: {}'.format(e))
