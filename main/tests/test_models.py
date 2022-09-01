from unittest import TestCase
from django.utils import timezone

from main.models import NewsletterUser


class NewsletterUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        NewsletterUser.objects.create(email='test_user123@example.com')

    def test_string_method(self):
        newsletter_user = NewsletterUser.objects.get(id=1)
        expected_string = f"{newsletter_user.email}"
        self.assertEqual(str(newsletter_user), expected_string)


class NewsletterUserTest(TestCase):

    def test_should_create_newsletter_user(self, email="test@user.com", joined=timezone.now()):
        return NewsletterUser.objects.create(email=email, joined=joined)

    def test_newsletter_user_creation(self):
        newsletter_user = self.test_should_create_newsletter_user()
        self.assertTrue(isinstance(newsletter_user, NewsletterUser))
        self.assertEqual(str(newsletter_user), newsletter_user.email)
