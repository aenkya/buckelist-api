from flask_testing import TestCase

from app import create_app

config_name = 'testing'


class TestConfig(TestCase):
    ''' test that app is initialized with right configurations '''
    def create_app():
        return create_app(config_name)

    def setUp(self):
        self.app = self.create_app()

    def test_config_is_testing(self):
        ''' test that app is initialized with testing configurations '''
        self.assertTrue(self.app.config['DEBUG'])
        self.assertEqual(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            'postgresql://bruce:Inline-360@localhost/test_db'
        )