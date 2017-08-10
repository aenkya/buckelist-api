from re import search
from flask import g
from flask_restplus import abort
from flask_httpauth import HTTPBasicAuth
from app.models.user import User
from instance.config import Config

auth = HTTPBasicAuth()