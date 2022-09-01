import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class NewsletterUserSerializerTestCase(APITestCase):
    def test_newsletter_user_creation(self):
        payload = {
            "email": "test_user11@example.com",
            "joined": datetime.datetime.now()
        }
        response = self.client.post(reverse("create_newsletter_user"), payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
