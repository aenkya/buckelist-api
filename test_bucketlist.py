import os
import unittest
import json

from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    '''This class represents the bucketlist test case'''

    def setUp(self):
        '''Define test variables and initialize app'''
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Skydive'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketlist_creation(self):
        '''Test API can create a bucketlist (POST request)'''
        res = self.client().post('/v1/bucketlists/', data=self.bucketlist)
        # check that the status code of the response is 201 (ok)
        self.assertEqual(res.status_code, 201)
        # check that the response's data has the given string data
        self.assertIn('Skydive', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        '''Test API can get bucketlists. (GET request)'''
        res = self.client().post('/v1/bucketlists/', data=self.bucketlist)
        res.assertEqual(res.status_code, 201)
        res = self.client().get('/v1/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Skydive', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        '''Test API can get individual bucketlist using its ID'''
        res = self.client().post('/v1/bucketlists/', data=self.bucketlist)
        res.assertEqual(res.status_code, 201)
        json_res_val = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/v1/bucketlists/{}', format(json_res_val['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Skydive', str(result.data))

    def test_bucketlist_can_be_edited(self):
        '''Test API can edit bucketlist details using its ID. (PUT request)'''
        res = self.client().post('/v1/bucketlists/', data=self.bucketlist)
        res.assertEqual(res.status_code, 201)
        json_res_val = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().put(
            '/v1/bucketlists/{}', format(json_res_val['id']), data={"Bungee"})
        self.assertEqual(res.status_code, 200)
        result = self.client().get(
            '/v1/bucketlists/{}', format(json_res_val['id']))
        self.assertIn('Bungee', str(result.data))

    def test_bucketlist_deletion(self):
        '''Test API can delete bucketlist
            using bucketlist ID. (DELETE request)'''
        res = self.client().post('/v1/bucketlists/', data=self.bucketlist)
        res.assertEqual(res.status_code, 201)
        res_val_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        del_res = self.client().delete(
            '/v1/bucketlists/{}', format(res_val_json['id']))
        self.assertEqual(del_res.status_code, 200)
        res = self.client().get(
            '/v1/bucketlists/{}', format(res_val_json['id']))
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        ''' Tear down all initialized variables'''
        with self.app.app_context():
            # remove db session
            db.session.remove()
            # drop all tables
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
