from django.urls import path, include
from django.views.generic import TemplateView

from .views import control_newsletter, control_newsletter_list, \
    control_newsletter_edit, control_newsletter_delete


app_name = 'control_panel'
urlpatterns = [
    path('newsletter/', control_newsletter, name='control_newsletter'),
    path('newsletter-list/', control_newsletter_list, name='control_newsletter_list'),
    path('newsletter-detail/<int:pk>', control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter-edit/<int:pk>', control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter-delete/<int:pk>', control_newsletter_delete, name='control_newsletter_delete'),

]
