from django.urls import path
from .views import PostListView, PostDetailView, FilterPostView, SearchPostView, post_detail, \
    post_list, category_detail, search, new_post, post_list_admin, \
    edit_post, delete_post, like_post

app_name = 'blog'
urlpatterns = [
    path('blog-list/', PostListView.as_view(), name='blog_list'),
    path('blog-detail/<slug:slug>/', PostDetailView.as_view(), name='blog_detail'),
    path('category-detail/<slug:slug>', category_detail, name='category_detail'),
    path('delete-post/<int:pk>/', delete_post, name='delete_post'),
    path('edit-post/<int:pk>/', edit_post, name='edit_post'),
    path('new-post/', new_post, name='new_post'),
    path('post-list/', post_list, name='post_list'),
    path('post-list-admin/', post_list_admin, name='post_list_admin'),
    path('post-detail/<slug:slug>/', post_detail, name='post_detail'),
    path('results/', search, name='search'),
    path('blog-list/filter', FilterPostView.as_view(), name='blog_list_filter'),
    path('blog-list/search', SearchPostView.as_view(), name='blog_list_search'),
    path('like-post/<int:pk>', like_post, name='like_post'),
]
