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
        result = json.loads(response.data)
        expected_list = sorted(['id', 'name', 'items', 'date_created', 'date_modified', 'created_by'])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([result.get('name'), result.get('created_by')], ['sample_1', 1])
