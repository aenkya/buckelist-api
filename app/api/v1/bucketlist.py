from flask import request, jsonify, g, url_for
from flask_restplus import abort, Resource, fields, Namespace, marshal_with
from flask_restplus import marshal
from sqlalchemy import desc
from app.models.bucketlist import Bucketlist
from app.models.user import User
from .item import item_fields
from app.utils.utilities import auth
from instance.config import Config


bucketlist_api = Namespace(
    'bucketlists', description='A bucketlist creation namespace')

bucketlist_fields = bucketlist_api.model(
    'Bucketlist',
    {
        'id': fields.Integer(),
        'name': fields.String(
            required=True,
            description="Bucketlist name",
            example="test_bucketlist"),
        'date_created': fields.DateTime(required=False, attribute='date_created'),
        'date_modified': fields.DateTime(required=False, attribute='date_modified'),
        'created_by': fields.Integer(required=True, attribute='user_id'),
        'items': fields.Nested(item_fields)
    }
)


@bucketlist_api.route('', endpoint='bucketlist')
class BucketlistsEndPoint(Resource):

    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successful Retreival of bucketlists')
    @bucketlist_api.response(400, 'No bucketlists found for specified user')
    @bucketlist_api.response(404, 'No bucketlists found for specified user')
    def get(self):
        ''' Retrieve bucketlists belonging to user '''
        auth_user = g.user
        search_term = request.args.get('q') or None
        limit = request.args.get('limit') or Config.MAX_PAGE_SIZE
        page_limit = 100 if int(limit) > 100 else int(limit)
        page = request.args.get('page') or 1

        if page_limit < 1 or page < 1:
            return abort(400, 'Page or Limit cannot be negative values')

        bucketlist_data = Bucketlist.query.filter_by(user_id=auth_user.id).\
            order_by(desc(Bucketlist.date_created))
        if bucketlist_data.all():
            bucketlists = bucketlist_data

            if search_term:
                bucketlists = bucketlist_data.filter(
                    Bucketlist.name.ilike('%'+search_term+'%')
                )

            bucketlist_paged = bucketlists.paginate(
                page=page, per_page=page_limit, error_out=True
            )
            results = dict(data=marshal(bucketlist_paged.items, bucketlist_fields))

            pages = {
                'page': page, 'per_page': page_limit,
                'total_data': bucketlist_paged.total, 'pages': bucketlist_paged.pages
            }

            if page == 1:
                pages['prev_page'] = url_for('api.bucketlist')+'?limit={}'.format(page_limit)

            if page > 1:
                pages['prev_page'] = url_for('api.bucketlist')+'?limit={}&page={}'.format(page_limit, page-1)

            if page < bucketlist_paged.pages:
                pages['next_page'] = url_for('api.bucketlist')+'?limit={}&page={}'.format(page_limit, page+1)

            results.update(pages)
            return results, 200

        return abort(400, message='No bucketlists found for specified user') 

    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(201, 'Bucketlist created successfully!')
    @bucketlist_api.response(409, 'Bucketlist already exists!')
    @bucketlist_api.response(500, 'Internal Server Error')
    @bucketlist_api.doc(model='Bucketlist', body=bucketlist_fields)
    def post(self):
        ''' Create a bucketlist '''
        arguments = request.get_json(force=True)
        name = arguments.get('name').strip()
        auth_user = g.user
        try:
            bucketlist = Bucketlist(name=name, user_id=auth_user.id)
            if bucketlist.save_bucketlist():
                return {'message': 'Bucketlist created successfully!'}, 201
            return abort(409, message='Bucketlist already exists!')
        except Exception as e:
            abort(400, message='Failed to create new bucketlist -> {}'.format(e.message))


@bucketlist_api.route('/<int:bucketlist_id>', endpoint='single_bucketlist')
class SingleBucketlistEndpoint(Resource):

    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @marshal_with(bucketlist_fields)
    @bucketlist_api.response(200, 'Successful retrieval of bucketlist')
    @bucketlist_api.response(400, 'No bucketlist found with specified ID')
    def get(self, bucketlist_id):
        ''' Retrieve individual bucketlist with given bucketlist_id '''
        auth_user = g.user
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, user_id=auth_user.id).first()
        if bucketlist:
            return bucketlist, 200
        abort(400, message='No bucketlist found with specified ID')

    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successfully Updated Bucketlist')
    @bucketlist_api.response(400, 'Bucketlist with id {} not found or not yours.')
    @bucketlist_api.marshal_with(bucketlist_fields)
    def put(self, bucketlist_id):
        ''' Update bucketlist with given bucketlist_id '''
        auth_user = g.user
        arguments = request.get_json(force=True)
        name = arguments.get('name').strip()

        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, user_id=auth_user.id).first()
        if bucketlist:
            bucketlist.name = name
            bucketlist.save_bucketlist()
            return bucketlist, 200
        else:
            abort(400, message='Bucketlist with id {} not found or not yours.'.format(
                bucketlist_id))

    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Bucketlist with id {} successfully deleted.')
    @bucketlist_api.response(400, 'Bucketlist with id {} not found or not yours.')
    def delete(self, bucketlist_id):
        ''' Delete bucketlist with bucketlist_id as given '''
        auth_user = g.user
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, user_id=auth_user.id).first()
        if bucketlist:
            if bucketlist.delete_bucketlist():
                response = {
                    'message': 'Bucketlist with id {} successfully deleted.'.format(bucketlist_id)}
            return response, 200
        else:
            abort(400, message='Bucketlist with id {} not found or not yours.'.format(
                bucketlist_id))
