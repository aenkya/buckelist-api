import json

from tests.base_test import BaseCase


class TestAuthenticateUser(BaseCase):

    def setUp(self):
        super(TestAuthenticateUser, self).setUp()

    def test_user_generate_auth_token_when_correct_login_credentials_are_provided(self):
        login_credentials = json.dumps(dict(
            email=self.user_1.get('email'), 
            password=self.user_2.get('password')
            ))
        path = '/api/v1/auth/login'
        response = self.client().post(path, data=login_credentials)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, 200)
