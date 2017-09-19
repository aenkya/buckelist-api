from tests.base_test import BaseCase
from app.models.user import User


class TestUserModel(BaseCase):
    ''' Tests for the user model '''

    def setUp(self):
        super(TestUserModel, self).setUp()

    def test_user_is_added_to_db(self):
        with self.app.app_context():
            self.user = User.query.filter_by(id=1, active=True).first().email
        self.assertEqual(
            self.user,
            'emugaya@andela.com',
            'User was not created'
            )

    def test_password_is_write_only(self):
        ''' check that password is not readable '''
        with self.app.app_context():
            user = User.query.filter_by(email="pnyondo@andela.com", active=True).first()
        self.assertEqual(user.password, 'Password: Write Only')

    def test_verify_password_returns_true_for_correct_password(self):
        with self.app.app_context():
            user = User.query.filter_by(email="emugaya@andela.com", active=True).first()
        self.assertTrue(
            user.verify_password('test'),
            'Password does not match user password stored in db'
        )


    def test_verify_password_returns_false_for_incorrect_password(self):
        with self.app.app_context():
            user = User.query.filter_by(email="emugaya@andela.com", active=True).first()
        self.assertFalse(
            user.verify_password('cow'),
            "Password doesnot match email so it should return false"
        )

    def test_no_repeated_users_added(self):
        
        with self.app.app_context():
            user = User(email='emugaya@andela.com', password="test")
            check = user.save_user()
        self.assertFalse(check, "User with identical attributes exists")

    def test_delete_user(self):
        with self.app.app_context():
            user = User.query.filter_by(
                first_name="Ezekiel", active=True).first()
        self.assertTrue(isinstance(user, User))
        with self.app.app_context():
            user.delete_user()
            verify_user = User.query.filter_by(
                first_name="Ezekiel", active=True).first()
        self.assertFalse(
            verify_user,
            "User that is deleted should not be returned"
        )