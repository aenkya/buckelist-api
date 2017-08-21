import json
import base64

from tests.base_test import BaseCase


class TestBucketlistEndpoint(BaseCase):
    ''' A class to test the bucketlist endpoints '''

    def setUp(self):
        super(BaseCase, self).setUp()
        self.bucketlist_data = {'name': 'Go fishing'}

    def test_post_bucketlists_adds_new_bucketlist(self):
        ''' add bucketlist with post route '''
        self.add_test_users()
        response = self.client().post(
            '/api/v1/bucketlists',
            data=json.dumps(self.bucketlist_data),
            headers=self.auth_headers())
        result = json.loads(reponse.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Bucketlist.query.all()), 1)
        self.assertEqual(result['message'], 'Bucketlist created successfully!')

    def test_get_bucketlists_returns_all_bucketlists_for_user(self):
        ''' get all buckets for specified user '''
        self.add_test_users()
        self.add_test_bucketlists()
        response = self.client().get(
            '/api/v1/bucketlists',
            header=self.auth_headers())
        result = json.loads(response.data).get('results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)

    def test_get_bucketlist_returns_bucketlist_for_specified_bucketlist_id(self):
        ''' GET api/v1/bucketlist/<bucketlist_id> returns single bucketlist '''
        self.add_test_users()
        self.add_test_bucketlists()
        response = self.client().get(
            '/api/v1/bucketlists/1',
            headers=self.auth_headers())
        result = json.loads(response.data)
        results_list = sorted(
            ['id', 'name', 'items', 'date_created', 'date_modified', 'user_id'])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            [result.get('name'), result.get('user_id')], ['Go fishing', 1])

    def test_edit_bucketlist_fields(self):
        self.add_test_users()
        self.add_test_bucketlists()
        response = self.client().get(
            '/api/v1/bucketlists/1',
            headers=self.auth_headers())
        result = json.loads(response.data)

        self.assertEqual(result.get('name'), 'Go fishing')

        update_fields = {'name': 'Visit Bali'}
        response = self.client().put(
            '/api/v1/bucketlists/1',
            data=json.dumps(update_fields),
            headers=self.auth_headers())
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('name'), update_fields.get('name'))

    def test_edit_fails_to_update_bucketlist_if_it_does_not_belong_to_the_user(self):
        self.add_test_users()
        self.add_test_bucketlists()

        other_user = User(
            first_name='Other',
            last_name='User',
            email='other@email.com',
            password='password')
        other_user.save_user()

        login_credentials = '{}:{}'.format('other@email.com', 'password')
        other_user_auth = {
            'Authorization': 'Basic ' + base64.b64encode(login_credentials)}

        update_fields = {'name': 'Skydive'}
        response = self.client().put(
            '/api/v1/bucketlists/1',
            data=json.dumps(update_fields),
            headers=other_user_auth)
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result.get('message'),
            'Bucketlist with ID#1 not found')

    def test_delete_removes_bucketlist_from_database(self):
        self.add_test_users()
        self.add_test_bucketlists()

        self.assertEqual(len(Bucketlist.query.all()), 2)

        response = self.client().delete(
            '/api/v1/bucketlists/1',
            headers=self.auth_headers())
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            result.get('message'),
            'Bucketlist with ID#1 successfully deleted.')
        self.assertEqual(len(Bucketlist.query.all()), 1)

    def test_delete_fails_with_400_error_if_bucketlist_does_not_belong_to_the_user(self):
        self.add_test_users()
        self.add_test_bucketlists()

        self.assertEqual(len(Bucketlist.query.all()), 2)

        other_user = User(
            first_name='Other',
            last_name='User',
            email='other@email.com',
            password='password')
        other_user.save_user()

        login_credentials = '{}:{}'.format('other@email.com', 'password')
        other_user_auth = {
            'Authorization': 'Basic ' + base64.b64encode(login_credentials)}

        response = self.client().delete('/api/v1/bucketlists/1',
                                        headers=other_user_auth)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result.get('message'),
            'Bucketlist with ID#1 not found or not yours.')
        self.assertEqual(len(Bucketlist.query.all()), 2)

    def test_search_returns_bucketlists_whose_name_matches_a_search_term(self):
        self.add_test_users()
        self.add_test_bucketlists()

        response = self.client().get(
            '/api/v1/bucketlists?q=Bucketlist',
            headers=self.auth_headers())
        result = json.loads(response.data.decode()).get('results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)

        response = self.client().get(
            '/api/v1/bucketlists?q=One',
            headers=self.auth_headers())
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)

    def test_pagination_of_bucketlists_when_you_pass_a_limit_parameter(self):
        self.add_test_users()
        self.add_test_bucketlists()

        response = self.client().get(
            '/api/v1/bucketlists?limit=1',
            headers=self.auth_headers())
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        expected_result = sorted(['results', 'next', 'total_pages', 'page', 'num_results'])
        self.assertListEqual(sorted(result.keys()), expected_result)
        self.assertEqual(len(result.get('results')), 1)
