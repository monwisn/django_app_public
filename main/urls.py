from django.urls import path
from .views import home_page, about, create_user_profile, user_profile, contact, \
    newsletter_signup, newsletter_unsubscribe, newsletter_users, newsletter_user_delete, \
    change_language, policy, accept_cookie_policy, cookie_banner, delete_user

# from .views import NewsletterUserListView, NewsletterUserDetailView
# from .api_views import CreateNewsletterUserApiView


app_name = 'main'
urlpatterns = [
    path('', home_page, name='home_page'),
    path('about/', about, name='about'),
    path('user/create/', create_user_profile, name='create_user_profile'),
    path('user/profile/', user_profile, name='user_profile'),
    path('delete-user/', delete_user, name='delete_user'),
    path('contact/', contact, name='contact'),
    path('newsletter/sign-up/', newsletter_signup, name='newsletter_sign_up'),
    path('newsletter/unsubscribe/', newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/users/', newsletter_users, name='newsletter_users'),
    path('newsletter/users-delete/<str:pk>/', newsletter_user_delete, name='newsletter_users_delete'),
    path('change-language/', change_language, name='change_language'),
    path('policy/', policy, name='policy'),
    path('accept-cookie-policy/', accept_cookie_policy, name='accept_cookie_policy'),
    path('cookie-banner/', cookie_banner, name='cookie_banner'),
    # path('newsletter/users/create/', CreateNewsletterUserApiView.as_view(), name='create_newsletter_user'),
    # path('newsletter/users/', NewsletterUserListView.as_view, name='newsletter_users'),
    # path('newsletter/users/<int:id>/', NewsletterUserDetailView.as_view, name='newsletter_user_detail'),
]
