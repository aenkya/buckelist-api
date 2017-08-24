import unittest

from app import create_app


class TestConfig(unittest.TestCase):
    ''' test that app is initialized with right configurations '''
    def create_app(self):
        return create_app(config_name='testing')

    def setUp(self):
        self.app = self.create_app()

    def test_config_is_testing(self):
        ''' test that app is initialized with testing configurations '''
        self.assertTrue(self.app.config['TESTING'])
        self.assertEqual(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            'postgresql://bruce:Inline-360@localhost/test_db'
        )