from http import HTTPStatus
from django.test import TestCase


class PostFormTest(TestCase):
    def test_login(self):
        self.client.login(username='test_user11', password='TestUser#11')

    def test_get(self):
        response = self.client.get("/blog/new-post/")

        # 302 because first redirect to login page before adding new post
        self.assertEqual(response.status_code, HTTPStatus.OK)  # status code 200
        self.assertTemplateUsed(response, 'blog/new_post.html')

    def test_post_success(self):
        response = self.client.post("/blog/new-post/")

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # status code 302

    def test_post_detail(self):
        response = self.client.get("/blog/post-detail/last/")
        no_response = self.client.get("/blog/post-detail/something/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
