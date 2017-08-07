""" Routes for Bucketlist Functionality"""
from flask import Blueprint, request, jsonify
from flask_restful import Resource, abort, fields
from app.models.bucketlist import Bucketlist
from app import db, api

bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.nested(item_fields),
    'date_created': fields.DateTime(attribute='date_created'),
    'date_modified': fields.DateTime(attribute='date_modified'),
    'created_by': fields.Integer(attribute='user_id')
}


@api.namespace('/', '<int:bucketlist_id>')
class BucketlistsEndPoint(Resource):
