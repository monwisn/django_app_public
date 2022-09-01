from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase


class SignInTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_010',
                                                         password='Test12345#test',
                                                         email='test010@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test_010', password='Test12345#test')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='Test12345#test')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test_010', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class SignInViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test010',
                                                         password='Test12345#test',
                                                         email='test010@example.com')

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post('/authentication/login/', {'username': 'test010', 'password': 'Test12345#test'})
        self.assertTrue(response.data['authenticated'])

    def test_wrong_username(self):
        response = self.client.post('/authentication/login/', {'username': 'wrong', 'password': 'Test12345#test'})
        self.assertFalse(response.data['authenticated'])

    def test_wrong_password(self):
        response = self.client.post('/authentication/login/', {'username': 'test010', 'password': 'wrong'})
        self.assertFalse(response.data['authenticated'])

