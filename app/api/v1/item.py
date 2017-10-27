from flask import Blueprint, request, jsonify, g
from flask_restplus import abort, Resource, fields, Namespace, marshal_with
from app.models.item import Item
from app.models.bucketlist import Bucketlist
from app.utils.utilities import auth

item_api = Namespace(
    'bucketlists', description='A bucketlist item manipulation namespace')

item_fields = item_api.model(
    'Item',
    {
        'id': fields.Integer(),
        'name': fields.String(
            required=True,
            description="Item description",
            example="test_bucketlist"),
        'date_created': fields.DateTime(required=False, attribute='date_created'),
        'date_modified': fields.DateTime(required=False, attribute='date_modified'),
        'bucketlist_id': fields.Integer(required=True),
        'done': fields.Boolean(),
        'active': fields.Boolean()
    }
)


@item_api.route('/<int:bucketlist_id>/items', endpoint='item')
class ItemEndpoint(Resource):

    @item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @item_api.response(201, 'Successful added item')
    @item_api.response(400, 'Failed to create item')
    @item_api.response(500, 'Internal Server Error')
    @item_api.response(404, 'Item not found')
    @item_api.doc(model='Item', body=item_fields)
    @item_api.marshal_with(item_fields)
    def post(self, bucketlist_id):
        ''' Add items to bucketlist '''
        auth_user = g.user
        arguments = request.get_json(force=True)
        name = arguments.get('name').strip() or None
        if not name:
            return abort(400, 'Name cannot be empty!')        

        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, user_id=auth_user.id, active=True).first()
        if bucketlist:
            try:
                item = Item(name=name, bucketlist_id=bucketlist.id)
                item.save_item()
                return item, 201
            except Exception as e:
                abort(400, message='Failed to create item -> {}'.format(e.message))
        else:
            abort(404, message='Bucketlist of id {} not found or does not '
                               'belong to you.'.format(bucketlist_id))

    @item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @item_api.response(200, 'Successfully retrieved items')
    @item_api.response(404, 'Bucketlist item with id {} not found in the database')
    @item_api.marshal_with(item_fields, as_list=True)
    def get(self, bucketlist_id):
        ''' retrieve bucketlist items '''
        auth_user = g.user
        bucketlist = Bucketlist.query.filter_by(
            user_id=auth_user.id, id=bucketlist_id, active=True).first()
        if bucketlist:
            items = Item.query.filter_by(bucketlist_id=bucketlist.id, active=True).all()
            return items, 200
        return abort(404, 'Bucketlist item with id {} not found in the database'.format(bucketlist_id))


@item_api.route('/<int:bucketlist_id>/items/<item_id>', endpoint='single_item')
class SingleItemEndpoint(Resource):

    @item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @item_api.response(200, 'Successfully Updated Bucketlist')
    @item_api.response(400, 'No existing bucketlist or bucketlist_item with the ids passed')
    @item_api.response(403, 'Failed to update item')
    @item_api.response(404, 'Item not found')  
    @item_api.marshal_with(item_fields)
    def put(self, bucketlist_id, item_id):
        ''' Modify the item details'''
        auth_user = g.user
        arguments = request.get_json(force=True)
        name, done = arguments.get('name') or None, arguments.get('done')

        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, user_id=auth_user.id, active=True).first()
        if bucketlist is None:
            return abort(400, message='Bucketlist item of id {} not found or does not '
                                      'belong to you.'.format(bucketlist_id))

        item = Item.query.filter_by(
            id=item_id, bucketlist_id=bucketlist.id, active=True).first()
        if item:
            try:
                if name:
                    item.name = name.strip()
                item.done = done if done is not None else item.done
                item.save()
                return item, 200
            except Exception as e:
                return abort(403, message='Failed to update item -> {}'.format(e.message))
        abort(404, message='Item with id {} not found.'.format(item_id))

    @item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @item_api.response(200, 'Item with id {} deleted successfully.')
    @item_api.response(404, 'Item with id {} not found.')
    def delete(self, bucketlist_id, item_id):
        ''' Delete the item with given id '''
        auth_user = g.user
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, user_id=auth_user.id, active=True).first()
        if bucketlist is None:
            return abort(400, message='Bucketlist item of id {} not found or does not '
                                      'belong to you.'.format(bucketlist_id))
        item = Item.query.filter_by(
            id=item_id, bucketlist_id=bucketlist.id, active=True).first()
        if item:
            try:
                item.delete_item()
                response = {
                    'message': 'Item with id {} deleted successfully.'.format(item_id)}
                return response, 200
            except Exception as e:
                return abort(400, message='Failed to delete item -> {}'.format(e.message))
        abort(404, message='Item with id {} not found.'.format(item_id))

    @item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @item_api.response(200, 'Successfully retrieved items')
    @item_api.response(404, 'Bucketlist item with id {} not found in the database')
    @item_api.marshal_with(item_fields)
    def get(self, bucketlist_id, item_id):
        ''' retrieve bucketlist items '''
        auth_user = g.user
        bucketlist = Bucketlist.query.filter_by(
            user_id=auth_user.id, id=bucketlist_id, active=True).first()
        if bucketlist is None:
            return abort(400, message='Bucketlist item of id {} not found or does not '
                                      'belong to you.'.format(bucketlist_id))
        item = Item.query.filter_by(
            id=item_id, bucketlist_id=bucketlist.id, active=True).first()
        if item:
            return item, 200
        return abort(404, 'Bucketlist item with id {} not found in the database'.format(bucketlist_id))
