import json

from tests.base_test import BaseCase
from app.models.bucketlist import Bucketlist


class TestBucketlistEndpoint(BaseCase):
    ''' A class to test the bucketlist endpoints '''
    def setUp(self):
        super(TestBucketlistEndpoint, self).setUp()
        self.bucketlist_data = {'name': 'Eat Sushi'}

    def test_post_bucketlists_adds_new_bucketlist(self):
        with self.app.app_context():
            response = self.client().post(
                '/api/v1/bucketlists',
                data=json.dumps(self.bucketlist_data))
        self.assertEqual(response.status_code, 201)
        self.assertEqual('Bucketlist created successfully!',
                         json.loads(response.data).get('message'))

    def test_get_returns_all_bucketlists_for_user(self):
        with self.app.app_context():
            response = self.client().get('/api/v1/bucketlists')
            result = response.data
        self.assertEqual(response.status_code, 200)

    def test_get_returns_one_bucketlist_if_id_is_specified(self):
        with self.app.app_context():
            self.add_test_bucketlists()
            response = self.client().get('/api/v1/bucketlists/1')
        result = json.loads(response.data.decode('utf-8'))
        expected_list = sorted(['id', 'name', 'items', 'date_created', 'date_modified', 'created_by'])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([result.get('name'), result.get('created_by')], ['sample_1', 1])

    def test_edit_updates_bucketlist_fields(self):
        self.add_test_bucketlists()
        response = self.client().get('/api/v1/bucketlists/1')
        result = json.loads(response.data)

        self.assertEqual(result.get('name'), 'sample_1')

        update_fields = {'name': 'Bungee Jump'}
        response = self.client().put('/api/v1/bucketlists/1', data=json.dumps(update_fields))
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('name'), update_fields.get('name'))

    def test_edit_fails_to_update_bucketlist_if_it_does_not_belong_to_the_user(self):
        self.add_test_bucketlists()

        other_user = User(first_name='Other', last_name='User', email='other@email.com', password='password')
        other_user.save()

        login_credentials = '{}:{}'.format('other@email.com', 'password')
        other_user_auth = {'Authorization': 'Basic ' + base64.b64encode(login_credentials)}

        update_fields = {'name': 'Bungee Jump'}
        response = self.client().put('/api/v1/bucketlists/1', data=json.dumps(update_fields))
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get('message'), 'Bucketlist with ID#1 not found or not yours.')

    def test_delete_removes_bucketlist_from_database(self):
        self.add_test_bucketlists()

        self.assertEqual(len(Bucketlist.query.all()), 2)

        response = self.client().delete('/api/v1/bucketlists/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('message'), 'Bucketlist with ID#1 successfully deleted.')
        self.assertEqual(len(Bucketlist.query.all()), 1)

    def test_search_returns_bucketlists_whose_name_matches_a_search_term(self):
        self.add_test_bucketlists()

        response = self.client().get('/api/v1/bucketlists?q=Bucketlist')
        result = json.loads(response.data.decode()).get('results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)

        response = self.client().get('/api/v1/bucketlists?q=One')
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)

    def test_pagination_of_bucketlists_when_you_pass_a_limit_parameter(self):
        self.add_test_bucketlists()

        response = self.client().get('/api/v1/bucketlists?limit=1')
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        expected_result = sorted(['results', 'next', 'total_pages', 'page', 'num_results'])
        self.assertListEqual(sorted(result.keys()), expected_result)
        self.assertEqual(len(result.get('results')), 1)