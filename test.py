from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

class Contractor(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
