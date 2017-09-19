import json
import base64

from tests.base_test import BaseCase
from app.models.item import Item


class TestItemEndpoint(BaseCase):
    ''' A class to test the items endpoints '''

    def test_post_adds_new_item_to_bucketlist(self):
        with self.app.app_context():

            self.assertEqual(len(Item.query.all()), 2)

            response = self.client().post('/api/v1/bucketlists/1/items',
                                          data=json.dumps(self.item_data),
                                          headers=self.auth_headers())
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['name'], 'Gokarting',
                         'Item name should be similar to given name')
        with self.app.app_context():
            self.assertEqual(len(Item.query.all()), 3)

    def test_get_returns_all_items_of_a_bucketlist(self):
        with self.app.app_context():
            response = self.client().get('/api/v1/bucketlists/1/items',
                                         headers=self.auth_headers())

        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(result), 2)

    def test_get_returns_an_item_when_item_id_is_provided(self):
        with self.app.app_context():

            response = self.client().get('/api/v1/bucketlists/1/items/1',
                                         headers=self.auth_headers())
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        actual_results = [result.get('name'), result.get('done')]
        self.assertListEqual(actual_results, ['Mombasa', False])

    def test_edit_updates_an_item_of_a_bucketlist(self):
        with self.app.app_context():

            response = self.client().get('/api/v1/bucketlists/1/items/1',
                                         headers=self.auth_headers())
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        actual_results = [result.get('name'), result.get('done')]
        self.assertListEqual(actual_results, ['Mombasa', False])

        update_item_fields = {'name': 'Updated Item', 'done': True}
        with self.app.app_context():
            response = self.client().put('/api/v1/bucketlists/1/items/1',
                                         data=json.dumps(update_item_fields),
                                         headers=self.auth_headers())
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        actual_results = [result.get('name'), result.get('done')]
        self.assertListEqual(actual_results, ['Updated Item', True])

    def test_edit_can_update_the_status_of_a_bucketlist_item_from_complete_to_incomplete(self):
        with self.app.app_context():
            complete_item = Item(name='Gokarting', bucketlist_id=1, done=True)
            complete_item.save()

        update_item_fields = {'done': False}
        with self.app.app_context():
            response = self.client().put('/api/v1/bucketlists/1/items/1',
                                         data=json.dumps(update_item_fields),
                                         headers=self.auth_headers())
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(result.get('done'))

    def test_delete_removes_item_from_bucketlist(self):
        with self.app.app_context():

            self.assertEqual(len(Item.query.filter_by(active=True).all()), 2)

            response = self.client().delete('/api/v1/bucketlists/1/items/1',
                                            headers=self.auth_headers())
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('message'),
                         'Item with id 1 deleted successfully.')
        with self.app.app_context():
            self.assertEqual(len(Item.query.filter_by(active=True).all()), 1)
