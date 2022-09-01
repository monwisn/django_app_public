from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='', null=True, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='default_user.jpg', upload_to='profile_pictures')
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user}"

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)


# newsletter subscribers
class NewsletterUser(models.Model):
    email = models.EmailField()
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('main:newsletter_sign_up', args=str(self.id))  # reverse('url_name', args=(obj.pk,))


class Newsletter(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    subject = models.CharField(max_length=200)
    # body = models.TextField(max_length=2000)
    body = RichTextField(null=True, blank=True)
    email = models.ManyToManyField(NewsletterUser)
    status = models.CharField(max_length=15, choices=EMAIL_STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.subject
