from tests.base_test import BaseCase
from app.models.user import User


class TestUserModel(BaseCase):
    ''' Tests for the user model '''

    def test_user_is_added_to_db(self):
        with self.app.app_context():
            user = User.query.filter_by(id=1).first().email
        self.assertEqual(
            user,
            'emugaya@andela.com',
            'User was not created'
            )