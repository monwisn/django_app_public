from django.test import TestCase
from django.template.defaultfilters import slugify
from django.utils import timezone

from blog.models import Post, Category
from main.models import NewsletterUser


class ModelsTestCase(TestCase):
    def test_post_has_slug(self):
        """Posts are given slugs correctly when saving"""
        post = Post.objects.create(title='Next post')
        post.author = 'test_user010'
        post.save()

        self.assertEqual(post.slug, slugify(post.title))


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        Category.objects.create(title='Test', description='test category model')

    def test_title_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_description_label_fail(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Description')

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_title_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_title_max_length_fail(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_description_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('description').max_length
        self.assertEqual(max_length, 300)

    def test_slug_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        # This will also fail if the urlconf is not defined
        self.assertEqual(category.get_absolute_url(), '/blog/category-detail/1')

    def test_get_absolute_url_fail(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), '/blog/category_detail/1')


