from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

routes = ['/', '/marketplace', '/home', '/home/removed', '/home/message_sent', '/send_message', '/messages']

class Contractor(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the homepage."""
        result = self.client.get(routes[0])
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Username', result.data)

    def test_market(self):
        """Test the markplace."""
        result = self.client.post(routes[1])
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Welcome to random market!', result.data)

    def test_home(self):
        """Test the home page."""
        result = self.client.post(routes[2])
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Post a new item', result.data)

    def test_home_removed(self):
        """Test the home page after removing an item."""
        result = self.client.post(routes[3])
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Post a new item', result.data)

    def test_message_sent(self):
        """Test the commenting."""
        result = self.client.post(routes[4])
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Post a new item', result.data)

    def test_messages(self):
        """Test the user messages."""
        result = self.client.post(routes[5])
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Leave comment and return to home', result.data)

if __name__ == '__main__':
    unittest_main()