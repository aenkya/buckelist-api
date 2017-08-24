import json

from tests.base_test import BaseCase

class TestAuthEndpoint(BaseCase):
    ''' A class to test the authentication tests '''

    def setUp(self):
        super(TestAuthEndpoint, self).setUp()
        self.user_data = {'first_name': 'First', 'last_name': 'Last', 'email': 'first@email.com',
                          'password': 'test_password', 'password_confirm': 'test_password'}

    def test_user_registration(self):
        response = self.client().post('/api/v1/auth/register', data = json.dumps(self.user_data))
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User registration successful.')

    def test_register_already_registered_user_unsuccessful(self):
        response = self.client().post('/api/v1/auth/register', data = json.dumps(self.user_data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/auth/register', data = json.dumps(self.user_data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(result['message'], 'User already Exists!. Login')

    def test_user_registration_unsuccessful_if_password_doesnt_match_confirmation(self):
        user_data = {'first_name': 'Joshua', 'last_name': 'Kagenyi', 'email': 'josh@andela.com',
                     'password': 'test', 'password_confirm': 'tester'}

        response = self.client().post('/api/v1/auth/register', data=json.dumps(user_data))
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Password doesn't match confirmation")

    def test_user_registration_fails_with_401_error_if_email_is_invalid(self):
        user_data = {'first_name': 'First', 'last_name': 'Last', 'email': 'test@com',
                     'password': 'test_password', 'password_confirm': 'test_password'}

        response = self.client().post('/api/v1/auth/register', data=json.dumps(user_data))
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], 'email address is invalid.')