from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .views import push_notification, send_push

urlpatterns = i18n_patterns(
    path('', include('main.urls')),
    path(_('admin/'), admin.site.urls),
    path('push_notification', push_notification, name='push_notification'),
    path('send_push', send_push),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('authentication/', include('authentication.urls')),
    path('blog/', include('blog.urls')),
    path('control/', include('control_panel.urls')),
    path('galleries/', include('galleries.urls')),
    prefix_default_language=False,
)
# ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if not settings.DEBUG:
    # handler = "app_name.views.function in views.py"
    handler403 = "plants_app.views.forbidden_403"
    handler404 = "plants_app.views.page_not_found_404"
    handler500 = "plants_app.views.error_500"
