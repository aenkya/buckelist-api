from datetime import datetime

from tests.base_test import BaseCase
from app.models.bucketlist import Bucketlist
from app.models.item import Item


class TestItemModel(BaseCase):

    def setUp(self):
        super(TestItemModel, self).setUp()

    def test_item_inserted_in_db(self):
        with self.app.app_context():
            item = Item.query.filter_by(id=1).first()
        self.assertEqual(item.name, "Mombasa", "Name not added")
        self.assertEqual(item.bucketlist_id, 1, "User Id not added")
        self.assertTrue(isinstance(item.date_created, datetime))
        self.assertTrue(isinstance(item.date_modified, datetime))

    def test_add_item_to_db(self):
        with self.app.app_context():
            bucketlist = Bucketlist.query.filter_by(name="sample_1").first()
            item = Item(
                name='Fishing',
                bucketlist_id=bucketlist.id
            )
            check = item.save_item()
        self.assertTrue(check, "Bucketlist item should be added")

    def test_delete_bucketlist_item(self):
        with self.app.app_context():
            item = Item.query.filter_by(id=1).first()
        self.assertTrue(item)
        with self.app.app_context():
            item.delete_item()
            verify_item = Item.query.filter_by(id=1).first()
        self.assertFalse(
            verify_item,
            "Item that is deleted should not exist in the database"
        )
