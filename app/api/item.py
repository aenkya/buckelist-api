""" Routes for bucket_item Functionality"""
# from flask import g
# from flask import Blueprint, request, jsonify
from flask_restplus import fields
# from app.models.bucketlist import Bucketlist
# from app import api

item_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime(attribute='created_at'),
    'date_modified': fields.DateTime(attribute='modified_at'),
    'done': fields.Boolean
}
