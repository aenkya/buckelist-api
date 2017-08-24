import json
import base64

from tests.base_test import BaseCase
from app.models.item import Item


class TestItemEndpoint(BaseCase):
    ''' A class to test the items endpoints '''

    def test_post_adds_new_item_to_bucketlist(self):
        self.add_test_users()
        self.add_test_bucketlists()

        self.assertEqual(len(Item.query.all()), 0)

        response = self.client().post(
            '/api/v1/bucketlists/1/items',
            data=json.dumps(self.item_data),
            headers=self.auth_headers())
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            result.get('message'),
            'Item successfully added to Bucketlist ID#1')
        self.assertEqual(len(Item.query.all()), 1)

    def test_get_returns_all_items_of_a_bucketlist(self):
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_items()

        response = self.client().get(
            '/api/v1/bucketlists/1/items',
            headers=self.auth_headers())
        result = json.loads(response.data.decode()).get('results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)

    def test_get_returns_an_item_when_item_id_is_provided(self):
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_items()

        response = self.client().get(
            '/api/v1/bucketlists/1/items/1',
            headers=self.auth_headers())
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        actual_results = [result.get('name'), result.get('done')]
        self.assertListEqual(actual_results, ['Gokarting', False])

    def test_edit_updates_an_item_of_a_bucketlist(self):
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_items()

        response = self.client().get('/api/v1/bucketlists/1/items/1',
                                     headers=self.auth_headers())
        result = json.loads(response.data.decode())
        actual_results = [result.get('name'), result.get('done')]
        self.assertListEqual(actual_results, ['Gokarting', False])

        update_item_fields = {'name': 'Updated Item', 'done': True}
        response = self.client().put(
            '/api/v1/bucketlists/1/items/1',
            data=json.dumps(update_item_fields),
            headers=self.auth_headers())
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        actual_results = [result.get('name'), result.get('done')]
        self.assertListEqual(actual_results, ['Updated Item', True])

    def test_edit_can_update_the_status_of_a_bucketlist_item_from_complete_to_incomplete(self):
        self.add_test_users()
        self.add_test_bucketlists()
        complete_item = Item(name='Gokarting', bucketlist_id=1, done=True)
        complete_item.save()

        update_item_fields = {'done': False}
        response = self.client().put('/api/v1/bucketlists/1/items/1', data=json.dumps(update_item_fields),
                                     headers=self.auth_headers())
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertFalse(result.get('done'))

    def test_delete_removes_item_from_bucketlist(self):
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_items()

        self.assertEqual(len(Item.query.all()), 3)

        response = self.client().delete('/api/v1/bucketlists/1/items/1',
                                        headers=self.auth_headers())
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('message'),
                         'Item with ID#1 deleted successfully.')
        self.assertEqual(len(Item.query.all()), 2)

    def test_all_actions_fail_with_403_error_if_bucketlist_does_not_belong_to_user(self):
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_items()

        user = User(first_name='Another', last_name='User',
                    email='another@email.com', password='test_password')
        user.save()
        login_credentials = '{}:{}'.format(
            'another@email.com', 'test_password')
        auth_headers = {'Authorization': 'Basic ' +
                        base64.b64encode(login_credentials)}

        response = self.client().post('/api/v1/bucketlists/1/items', data=json.dumps(self.item_data),
                                      headers=auth_headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get(
            'message'), 'Bucketlist of ID#1 not found')

        response = self.client().get('/api/v1/bucketlists/1/items',
                                     headers=auth_headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get(
            'message'), 'Bucketlist of ID#1 not found')

        response = self.client().get('/api/v1/bucketlists/1/items/1',
                                     headers=auth_headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get(
            'message'), 'Bucketlist of ID#1 not found')

        update_item_fields = {'name': 'Updated Item', 'done': True}
        response = self.client().put('/api/v1/bucketlists/1/items/1', data=json.dumps(update_item_fields),
                                     headers=auth_headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get(
            'message'), 'Bucketlist of ID#1 not found')

        response = self.client().delete('/api/v1/bucketlists/1/items/1',
                                        headers=auth_headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get(
            'message'), 'Bucketlist of ID#1 not found')
