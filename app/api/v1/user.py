from flask import request, g
from flask_restplus import abort, Resource, Namespace, fields, abort, reqparse
from app.models.user import User
from sqlalchemy import desc
from app.utils.utilities import validate_email, auth


user_api = Namespace(
    'users', description='User details')

user_fields = user_api.model(
    'User',
    {   
        'id': fields.Integer(required=True, description='User ID', example='1'),
        'first_name': fields.String(
            required=True, description='User first name', example='fName'),
        'last_name': fields.String(
            required=True, description='User last name', example='lName'),
        'email': fields.String(
            required=True, description='User email', example='lname@test.com'),
        'bucketlists_url': fields.Url(
            'api.bucketlist', absolute=True),
    })

@user_api.route('', endpoint='users')
class UsersList(Resource):
    @auth.login_required
    @user_api.marshal_with(user_fields)
    def get(self):
        ''' Method to retrieve all users '''
        use_token = request.headers.get('use_token') or None

        if use_token:
            return g.user
        users = User.query.order_by(desc(User.date_created)).all()
        return users, 200

@user_api.route('/<user_id>', endpoint='single_user')
class UserEndpoint(Resource):
    ''' Class for User Details '''
    @user_api.response(201, 'User details fetched successfully!')
    @user_api.response(400, 'User not found')
    @user_api.response(500, 'Server Error. Couldn\'t complete request')
    @user_api.doc(model='User', body=user_fields)
    @auth.login_required
    @user_api.header('x-access-token', 'Access Token', required=True)
    @user_api.marshal_with(user_fields)
    def get(self, user_id):
        ''' GET method to retrieve user details '''
        user = User.query.get(user_id)
        return user, 200 if user else abort(400, message='User with ID {} not found.'.format(user_id))

    @auth.login_required
    def delete(self, user_id):
        ''' A method to delete a user '''
        user = User.query.get(user_id)
        response = {'message': 'User with ID {} successfully deleted'.format(user_id)}
        return response, 200 if user.delete_user() else abort(400, message='User with ID {} not found'.format(user_id))
