import json
from flask_bcrypt import Bcrypt
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired
)

from app.models.baseModel import BaseModel, db
from instance.config import Config

bcrypt = Bcrypt()


class User(BaseModel):
    '''This class represents the user model'''
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    _password_hash = db.Column(db.String(255))

    @property
    def password(self):
        ''' Method that is run when password property is called '''
        return 'Password: Write Only'

    @password.setter
    def password(self, password):
        ''' Generate password hash '''
        self._password_hash = bcrypt.generate_password_hash(
            password, Config.BCRYPT_LOG_ROUNDS).decode()

    def exists(self):
        ''' Check if user exists '''
        return True if User.query.filter_by(email=self.email).first() else False

    def verify_password(self, password):
        ''' Method to verify that user's password matches password provided '''
        return bcrypt.check_password_hash(self._password_hash, password)

    def generate_auth_token(self, duration=Config.AUTH_TOKEN_DURATION):
        ''' Method for generating a JWT authentication token '''
        serializer = Serializer(Config.SECRET_KEY, expires_in=int(duration))
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_authentication_token(token):
        ''' Method to verify authentication token '''
        serializer = Serializer(Config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return data['id'] if data['id'] else False

    def delete_user(self):
        ''' Method to delete user '''
        if self.exists():
            self.delete()
            return True
        return False

    def save_user(self):
        ''' Method to save user '''
        if not self.exists():
            self.save()
            return True
        return False

    def __repr__(self):
        return '<User %r>' % self.name()

    def __str__(self):
        return '{0}'.format(self.name())
