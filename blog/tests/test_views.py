from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('127.0.0.1:8000')

        self.assertEqual(response.status_code, 200)

    def test_index_loads_fail(self):
        """The index page doesn't load properly"""
        response = self.client.get('127.0.0.1:8000')

        self.assertEqual(response.status_code, 404)

