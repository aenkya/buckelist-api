import json

from tests.base_test import BaseCase

class TestRegister(BaseCase):
    ''' A class of registration tests'''
    def setUp(self):
        super(TestRegister, self).setUp()
        self.user_data = {'first_name': 'First', 'last_name': 'Last', 'email': 'first@email.com',
                          'password': 'test_password', 'password_confirm': 'test_password'}

    def test_user_registration(self):
        response = self.client().post('/api/v1/auth/register', data = json.dumps(self.user_data))
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'User registration successful.')

    def test_register_already_registered_user_unsuccessful(self):
        response = self.client().post('/api/v1/auth/register', data = json.dumps(self.user_data))
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/auth/register', data = json.dumps(self.user_data))
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(result['message'], 'User already Exists!. Login')

    def test_user_registration_unsuccessful_if_password_doesnt_match_confirmation(self):
        user_data = {'first_name': 'Joshua', 'last_name': 'Kagenyi', 'email': 'josh@andela.com',
                     'password': 'test', 'password_confirm': 'tester'}

        response = self.client().post('/api/v1/auth/register', data=json.dumps(user_data))
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Password doesn't match confirmation")

    def test_user_registration_fails_with_401_error_if_email_is_invalid(self):
        user_data = {'first_name': 'First', 'last_name': 'Last', 'email': 'test@com',
                     'password': 'test_password', 'password_confirm': 'test_password'}

        response = self.client().post('/api/v1/auth/register', data=json.dumps(user_data))
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'], 'email address is invalid.')

class TestAuth(BaseCase):
    ''' A class of authentication tests '''
    def setUp(self):
        super(TestAuth, self).setUp()
        self.user_data = {'first_name': 'Ezekiel', 'last_name': 'Mugaya', 'email': 'emugaya@andela.com',
                 'password': 'test', 'password_confirm': 'test'}

    def test_token_generated_when_correct_login_credentials_are_provided(self):
        login_details = json.dumps(dict(email=self.user_data.get('email'), password=self.user_data.get('password')))
        auth_response = self.client().post('/api/v1/auth/login', data=login_details)
        self.assertIn('token', auth_response.data.decode('utf8').strip())
        self.assertEqual(auth_response.status_code, 200)

    def test_user_gets_400_error_if_the_login_credentials_are_incorrect(self):
        login_details = json.dumps(dict(email='wrong@email.com', password='wrong_password'))
        auth_response = self.client().post('/api/v1/auth/login', data=login_details)
        self.assertEqual(auth_response.status_code, 400)

    def test_user_gets_401_error_if_the_password_is_wrong(self):
        login_details = json.dumps(dict(email='pnyondo@andela.com', password='wrong_password'))
        auth_response = self.client().post('/api/v1/auth/login', data=login_details)
        self.assertEqual(auth_response.status_code, 401)
        result = json.loads(auth_response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Wrong password')