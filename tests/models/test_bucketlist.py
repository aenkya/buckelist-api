from datetime import datetime

from tests.base_test import BaseCase
from app.models.user import User
from app.models.bucketlist import Bucketlist


class TestBucketlistModel(BaseCase):

    def setUp(self):
        super(TestBucketlistModel, self).setUp()

    def Bucketlist_inserted_in_db(self):
        with self.app.app_context():
            bucketlist = Bucketlist.query.filter_by(id=1, active=True).first()
        self.assertEqual(bucketlist.name, "Bucketlist", "Name not added")
        self.assertEqual(bucketlist.user_id, 1, "user_id not added")
        self.assertTrue(isinstance(bucketlist.date_created, datetime))
        self.assertTrue(isinstance(bucketlist.date_modified, datetime))

    def test_add_bucketlist(self):
        with self.app.app_context():
            user = User.query.filter_by(email="pnyondo@andela.com", active=True).first()
            bucketlist = Bucketlist(name='Go hard or go home', user_id=user.id)
            check = bucketlist.save_bucketlist()
        self.assertTrue(check, "Bucketlist should be added")

    def test_no_repeat_bucketlist_names(self):
        with self.app.app_context():
            user = User.query.filter_by(email="pnyondo@andela.com", active=True).first()
            bucketlist = Bucketlist(name='sample_1', user_id=user.id)
            check = bucketlist.save_bucketlist()
        self.assertFalse(check, "Bucketlist should not be added")
        self.assertFalse(bucketlist.id)

    def test_delete_bucketlist(self):
        with self.app.app_context():
            bucketlist = Bucketlist.query.filter_by(
                name="sample_1", active=True).first()
        self.assertTrue(isinstance(bucketlist, Bucketlist))
        with self.app.app_context():
            bucketlist.delete_bucketlist()
            verify_bucketlist = Bucketlist.query.filter_by(
                name="sample_1", active=True).first()
        self.assertFalse(
            verify_bucketlist,
            "Bucketlist that is deleted should not be returned"
        )

    def test_deep_delete_bucketlist_deletes_from_db(self):
        with self.app.app_context():
            bucketlist = Bucketlist.query.filter_by(
                name="sample_1", active=True).first()
        self.assertTrue(isinstance(bucketlist, Bucketlist))
        with self.app.app_context():
            bucketlist.delete_bucketlist(True)
            verify_bucketlist = Bucketlist.query.filter_by(
                name="sample_1").first()
        self.assertFalse(
            verify_bucketlist,
            "Bucketlist that is deleted should not exist in the database"
        )

    def Bucketlist_item_list(self):
        with self.app.app_context():
            bucketlist = Bucketlist.query.filter_by(name="sample_1", active=True).first()
        self.assertTrue(isinstance(bucketlist.bucketlist_items, list))
