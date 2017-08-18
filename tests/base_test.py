from flask_testing import TestCase
from datetime import date
import json

from app import db, create_app
from app.models.user import User


class BaseCase(TestCase):
    ''' A class detailing the base properties to be inherited '''
    @staticmethod
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        super(BaseCase, self).setUp()
        self.app = self.create_app()
        self.client = self.app.test_client

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

        self.populate_db()

    def populate_db(self):
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_items()

    @staticmethod
    def add_test_users():
        ''' method to add test users to db '''
        user_1 = User(
            first_name: 'Ezekiel',
            last_name: 'Mugaya',
            email: 'emugaya@andela.com',
            password: 'test',
            confirm_password: 'test'
        )
        user_2 = User(
            first_name: 'Paul',
            last_name: 'Nyondo',
            email: 'pnyondo@andela.com',
            password: 'test',
            confirm_password: 'test'
        )
        user_1.save_user()
        user_2.save_user()

    @staticmethod
    def add_test_bucketlists():
        ''' method to add test bucketlists to db '''
        user = User.query.filter_by(email='pnyondo@andela.com').first()
        bucketlist_1 = Bucketlist(user_id=user.id, name='sample_1')
        bucketlist_2 = Bucketlist(user_id=user.id, name='sample_2')
        bucketlist_1.save(), bucketlist_2.save()

    @staticmethod
    def add_test_items():
        ''' method to add test items to bucketlist '''
        bucketlist = Bucketlist.query.filter_by(name='sample_1').first()
        item_1 = Item(name='Mombasa', bucketlist_id=bucketlist.id)
        item_2 = Item(name='kampala', bucketlist_id=bucketlist.id)
        item_1.save(), item_2.save()

    def auth_headers(self, email='pnyondo@andela.com', password='test'):
        ''' method generates auth headers for test user '''
        path = '/api/v1/auth/login'
        data = {'email': email, 'password': password}
        response = self.post_data(path, data)
        result = json.loads(response.data)
        self.assertTrue(result['auth_token'])
        return {'x-access-token': result['auth_token']}

    def post_data(self, path, data):
        ''' method to pass data to API path given '''
        return self.client.post(
            path,
            data=json.dumps(data),
            content_type='application/json',
            follow_directs=True
        )

    def tearDown(self):
        super(BaseCase, self).tearDown()
        db.session.remove()
        db.drop_all()
