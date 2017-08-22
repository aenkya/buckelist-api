""" Routes for Bucketlist Functionality"""
from flask import request, jsonify
from flask_restplus import Resource, fields, Namespace
from app.models.bucketlist import Bucketlist
from .item import item_fields


bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.Nested(item_fields),
    'date_created': fields.DateTime(attribute='date_created'),
    'date_modified': fields.DateTime(attribute='date_modified'),
    'created_by': fields.Integer(attribute='user_id')
}

bucketlist_api = Namespace('bucketlists', description='A bucketlist creation namespace')


@bucketlist_api.route('/', '/<int:bucketlist_id>')
class BucketlistsEndPoint(Resource):

    def get(self, bucketlist_id):
        ''' Retrieve bucketlist by id '''
        bucketlists = Bucketlist.get_all()
        results = []

        for bucketlist in bucketlists:
            obj = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    def post(self, user, *arg, **kwargs):
        ''' Create a bucketlist '''
        name = str(request.data.get('name', ''))
        if name:
            bucketlist = Bucketlist(name=name)
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 201
            return response
