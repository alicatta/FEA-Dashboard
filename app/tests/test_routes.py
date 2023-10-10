from app import app
import unittest

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_dashboard_route(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
