from unittest import TestCase

from rest_framework.reverse import reverse

from main.models import NewsletterUser


class NewsletterUserListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_newsletter_users = 20
        for newsletter_user_id in range(number_of_newsletter_users):
            NewsletterUser.objects.create(email=f'test_user{newsletter_user_id}@example.com')

    def test_url_exists(self):
        response = self.client.get("/newsletter/users")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('newsletter_users'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('newsletter_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/newsletter/newsletter_users_list.html')

    def test_pagination_is_correct(self):
        response = self.client.get(reverse('newsletter_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['newsletter_users']), 10)

