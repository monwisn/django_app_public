import string
import random

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now, timedelta
from django.http import HttpResponseRedirect


class CheckAgeMixin:
    def is_older_than(self, n=1):
        delta = timedelta(days=n)
        return now() - self.created > delta


class Timestamped(models.Model, CheckAgeMixin):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_random_text(n):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(n))


class SlugMixin(models.Model):
    SLUG_BASE_FIELD = 'title'
    SLUG_SUFFIX_LEN = 5
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    # self.title = None

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            slug = slugify(getattr(self, self.SLUG_BASE_FIELD))
            slugs = self.__class__.objects.filter(slug=slug).values_list("slug", flat=True)
            if slugs:
                while True:
                    if slug in slugs:
                        slug += get_random_text(self.SLUG_SUFFIX_LEN)
                    else:
                        break
            self.slug = slug
        return super().save(*args, **kwargs)


# Cookie Decorator

def cookie_policy(func):
    """
    This decorator can be used to redirect the visitor to the cookie policy page
    when it has not been accepted
    """
    def wrapper(request, *args, **kwargs):
        if request.COOKIES.get('cookie_accepted', False):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('main:cookie_policy'))

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__

    return wrapper


# Cookie Law Decorator

def cookie_law(func):
    def wrapper(request, *args, **kwargs):
        if request.GET.get('cookie_accepted', None):
            return func(request, *args, **kwargs)
        if request.COOKIES.get('cookie_law', False):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/en/european-cookie-law')

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
