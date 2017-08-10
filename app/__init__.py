from flask import Flask, Blueprint, abort
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy


from instance.config import app_config

# Create db instance
db = SQLAlchemy()

# Create v1 blueprint for api
api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(api_v1, version='1.0', title='BucketList API',
          description='api to allow the creation & control of bucketlists')


ns = api.namespace('bucketlists', description='Bucketlists operations')
api.init_app(api_v1)

BUCKETLISTS = {}


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(api_v1)
    db.init_app(app)

    return app


def abort_if_bucketlist_doesnt_exist(bucketlist_id):
    '''abort with 404 if bucketlist doesnt exist'''
    from app.models.bucketlist import Bucketlist
    bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
    if not bucketlist:
        abort(404)
