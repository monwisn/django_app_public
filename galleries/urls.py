from django.urls import path

from .views import galleries_list, gallery_details, add_gallery, add_photos, gallery_edit, \
    gallery_delete, galleries_list_admin, galleries_list_view, photos_view, photo_edit, photo_delete


app_name = "galleries"
urlpatterns = [
    path('', galleries_list, name="list"),
    path('add-gallery/', add_gallery, name='add_gallery'),
    path('<int:gallery_id>', gallery_details, name="details"),
    path('<int:gallery_id>/add/', add_photos, name='add_photos'),
    path('gallery-edit/<int:pk>', gallery_edit, name='gallery_edit'),
    path('gallery-delete/<int:pk>', gallery_delete, name='gallery_delete'),
    path('galleries-list-admin/', galleries_list_admin, name='galleries_list_admin'),
    path('galleries-list-view/', galleries_list_view, name='galleries_list_view'),
    path('galleries-list-view/<int:gallery_id>', photos_view, name='photos_view'),

    path('photo-edit/<int:pk>', photo_edit, name='photo_edit'),
    path('photo-delete/<int:pk>', photo_delete, name='photo_delete'),
]
