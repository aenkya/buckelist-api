from re import search
from flask import g, request
from flask_httpauth import HTTPTokenAuth
from app.models.user import User

auth = HTTPTokenAuth(scheme='Token')


def validate_email(email):
    ''' Method to check that a valid email is provided '''
    email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if search(email_re, email) else False

@auth.verify_token
def verify_token(token=None):
    ''' Method to verify token '''
    token = request.headers.get('x-access-token') or ''
    user_id = User.verify_authentication_token(token)
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
        return True
    return False
