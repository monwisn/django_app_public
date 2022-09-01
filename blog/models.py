from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from main.common import Timestamped, SlugMixin


class Category(Timestamped, SlugMixin):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=str(self.id))

    def __str__(self):
        return self.title


class Post(Timestamped, SlugMixin):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft')
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, default='Gdansk')
    category = models.ForeignKey(Category, default='new', on_delete=models.SET_DEFAULT)
    slug = models.SlugField(max_length=200, unique=True)
    file = models.FileField(upload_to='blog/files/', blank=True, null=True)
    image = models.ImageField(upload_to='blog/images/%Y/%m/%d/')
    image_width = models.IntegerField(blank=True, null=True, editable=False)
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)
    likes = models.ManyToManyField(User, related_name='likes')
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def num_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        # if not self.slug:
        #     self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return f'post {self.id}: "{self.title}"'


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', default=None)
    images = models.ImageField(upload_to='blog/images_all/', null=True, blank=True)

