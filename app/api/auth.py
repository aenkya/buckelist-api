from flask import Blueprint
from flask_restplus import abort, Resource, Namespace, fields, marshal
from app.models.user import User

auth = Namespace('auth', description='User authentication and registration')

USER = auth.model(
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


@auth.route('/register', endpoint='register')
class RegisterUser(Resource):
    ''' Class for User Registration '''
    @auth.response(201, {'message': 'User registered successfully'})
    @auth.response(401, {'message': 'Error while creating your account'})
    @auth.response(409, {'message': 'User already exists!'})
    @auth.response(500, {'message': 'Server Error. Couldn\'t complete request'})
    @auth.doc(model='User', body=USER)
    def post(self):
        ''' Method to handle POST request for User registration '''
        arguments = request.get_json(force=True)
        first_name, last_name, email = arguments.get(
            'first_name'), arguments.get('last_name', arguments.get('email'))
        password, password_confirm = arguments.get(
            'password'), arguments.get('password_confirm')

        
