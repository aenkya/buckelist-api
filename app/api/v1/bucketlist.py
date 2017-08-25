from flask import request, jsonify, g
from flask_restplus import abort, Resource, fields, Namespace, marshal_with
from app.models.bucketlist import Bucketlist
from app.models.user import User
from .item import item_fields


bucketlist_api = Namespace('bucketlists', description='A bucketlist creation namespace')

bucketlist_fields = bucketlist_api.model(
    'Bucketlist',
    {
        'id':fields.Integer(),
        'name': fields.String(
            required=True,
            description="Bucketlist name",
            example="test_bucketlist"),
        'date_created': fields.DateTime(required=False, attribute='date_create'),
        'date_modified': fields.DateTime(required=False, attribute='date_modified'),
        'created_by':fields.Integer(required=True, attribute='user_id'),
        'bucketlist_items': fields.Nested(item_fields)
    }
)

@bucketlist_api.route('', endpoint='bucketlist')
class BucketlistsEndPoint(Resource):

    @marshal_with(bucketlist_fields)
    def get(self):
        ''' Retrieve bucketlists belonging to user '''
        # auth_user = g.user
        bucketlists = Bucketlist.query.filter_by(user_id=1).all()
        if bucketlists:
            return bucketlists, 200
        abort(400, message='No bucketlists found for specified user')

    def post(self):
        ''' Create a bucketlist '''
        arguments = request.get_json(force=True)
        name = arguments.get('name')
        try:
            # user = User(email='email@email.com', first_name='email', last_name='lamail', password='123')
            # user.save_user()
            bucketlist = Bucketlist(name=name, user_id=1)
            if bucketlist.save_bucketlist():
                return {'message': 'Bucketlist created successfully!'}, 201
            return abort(409, message='Bucketlist already exists!')
        except Exception as e:
            abort(400, message='Failed to create new bucketlist -> {}'.format(e.message))


@bucketlist_api.route('/<int:bucketlist_id>', endpoint='single_bucketlist')
class SingleBucketlistEndpoint(Resource):
    @marshal_with(bucketlist_fields)
    def get(self, bucketlist_id):
        ''' Retrieve individual bucketlist with given bucketlist_id '''
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id, user_id=1).first()
        if bucketlist:
            return bucketlist, 200
        abort(400, message='No bucketlist found with specified ID')

    @marshal_with(bucketlist_fields)
    def put(self, bucketlist_id):
        ''' Update bucketlist with given bucketlist_id '''
        arguments = request.get_json(force=True)
        name = arguments.get('name')

        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id, user_id=1).first()
        if bucketlist:
            bucketlist.name = name
            bucketlist.save_bucketlist()
            return bucketlist, 200
        else:
            abort(400, message='Bucketlist with ID#{} not found or not yours.'.format(bucketlist_id))

    def delete(self, bucketlist_id):
        ''' Delete bucketlist with bucketlist_id as given '''
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id, user_id=1).first()
        if bucketlist:
            if bucketlist.delete_bucketlist():
                response = {'message': 'Bucketlist with ID#{} successfully deleted.'.format(bucketlist_id)}
            return response, 200
        else:
            abort(400, message='Bucketlist with ID#{} not found or not yours.'.format(bucketlist_id)) 

        



