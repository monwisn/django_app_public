import unittest
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By

from main.models import NewsletterUser


class SimpleTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home_page.html')

    def test_about_status_code(self):
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')

    def test_contact_status_code(self):
        response = self.client.get("/contact/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')



# views test
    def test_newsletter_user_list(self):
        newsletter_user = self.create_newsletter_user()
        url = reverse("newsletter_user.views.newsletter_user")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(newsletter_user.email, resp.content)



class TestSignup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_signup_fire(self):
        self.driver.get("http://localhost:8000/newsletter/sign-up/")
        self.driver.find_element(By.ID, 'id_email').send_keys("wisniewska.monika0@gmail.com")
        self.driver.find_element(By.ID, 'submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()
