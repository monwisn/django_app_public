from django.contrib.auth.models import User
from django.db import models
from main.common import Timestamped, SlugMixin
from tinymce import models as tinymce_models


class Status(models.IntegerChoices):
    HIDE = 1, "Hide"
    PUBLISHED = 2, "Published"


class Gallery(Timestamped, SlugMixin):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # description = tinymce_models.HTMLField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=Status.PUBLISHED, choices=Status.choices)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "gallery"
        verbose_name_plural = "Galleries"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if self.status == Status.HIDE:
        #     self.photos.update(status=Status.HIDE)
        super().save(*args, **kwargs)


def upload_to(instance, filename):
    return f"galleries/{instance.gallery.slug}/{filename}"


class Photo(Timestamped, SlugMixin):
    STATUS_CHOICES = (
        ('Once every 2-3 days', 'Once every 2-3 days'),
        ('Once a week', 'Once a week'),
        ('Once every 2 weeks', 'Once every 2 weeks'),
    )
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    how_often = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Once a week')
    image = models.ImageField(upload_to=upload_to)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="photos")
    source = models.CharField(max_length=512, null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=Status.PUBLISHED, choices=Status.choices)
    send_reminder = models.BooleanField(default=False, verbose_name='Send reminder to email')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == Status.PUBLISHED
