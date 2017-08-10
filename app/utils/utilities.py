from re import search
from flask import g
from flask_restplus import abort
from flask_httpauth import HTTPBasicAuth
from app.models.user import User
from instance.config import Config

auth = HTTPBasicAuth()


def validate_email(email):
	''' Method to check that a valid email is provided '''
    email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if search(email_re, email) else False

@auth.verify_token
def verify_token(token=None):
    ''' Method to verify token '''
    token = request.headers.get('x-access-token')
    user_id = User.verify_authentication_token(token)
    if user_id:
        g.current_user = User.query.filter_by(id=user.id).first()
        return True
    return False
