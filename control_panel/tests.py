from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import control_newsletter, control_newsletter_list, control_newsletter_edit, control_newsletter_delete


class TestUrls(SimpleTestCase):

    def test_newsletter_url_resolves(self):
        url = reverse('control_panel:control_newsletter')
        print(resolve(url))
        self.assertEquals(resolve(url).func, control_newsletter)

    def test_newsletter_list_url_resolves(self):
        url = reverse('control_panel:control_newsletter_list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, control_newsletter_list)

    def test_newsletter_edit_url_resolves(self):
        url = reverse('control_panel:control_newsletter_edit', args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, control_newsletter_edit)

    def test_newsletter_delete_url_resolves(self):
        url = reverse('control_panel:control_newsletter_delete', args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, control_newsletter_delete)

