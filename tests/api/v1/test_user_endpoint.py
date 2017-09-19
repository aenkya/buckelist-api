import json

from tests.base_test import BaseCase
from app.models.user import User


class TestUserEndpoint(BaseCase):
    ''' A class to test the user endpoints '''
    def setUp(self):
        super(TestUserEndpoint, self).setUp()

    def test_get_returns_all_users(self):
        with self.app.app_context():
            response = self.client().get('/api/v1/users',
                                         headers=self.auth_headers())
            result = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(result)), 2)

    def test_get_returns_one_user_if_id_is_specified(self):
        with self.app.app_context():
            response = self.client().get('/api/v1/users/1',
                                         headers=self.auth_headers())
        result = json.loads(response.data.decode('utf-8'))
        expected_list = sorted(['id', 'first_name', 'last_name', 'email', 'bucketlists_url'])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([result.get('first_name'), result.get('last_name')], ['Ezekiel', 'Mugaya'])


    def test_get_returns_auth_user_if_use_token_header_set(self):
        with self.app.app_context():
            headers = self.auth_headers()
            headers['use_token'] = True
            response = self.client().get('/api/v1/users',
                                         headers=headers)
        result = json.loads(response.data.decode('utf-8'))
        expected_list = sorted(['id', 'first_name', 'last_name', 'email', 'bucketlists_url'])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([result.get('first_name'), result.get('last_name')], ['Ezekiel', 'Mugaya'])


    def test_delete_user(self):
        with self.app.app_context():

            self.assertEqual(len(User.query.filter_by(active=True).all()), 2)

            response = self.client().delete('/api/v1/users/1',
                                            headers=self.auth_headers())
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('message'), 'User with ID 1 successfully deleted')
        with self.app.app_context():
            self.assertEqual(len(User.query.filter_by(active=True).all()), 1)
