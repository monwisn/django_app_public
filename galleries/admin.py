from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.db.models import Count
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from .models import Gallery, Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'gallery', 'status', 'how_often', 'send_reminder', 'created', 'updated', 'source']


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            t = get_thumbnail(value, "150")
            output.append(f"<a href='{value.url}' target='_blank'><img src='{t.url}'><a/>")
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        # return mark_safe(''.join(output))
        return ''.join(output)


class PhotoInline(admin.StackedInline):
    model = Photo
    fields = ["title", "short_description", "image", "status", "how_often", "send_reminder"]
    # readonly_fields = ["slug"]
    extra = 1
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}


class HasPhotosFilter(admin.SimpleListFilter):
    title = "Number of photos"
    parameter_name = "photos_count"

    def lookups(self, request, model_admin):
        return (
            ("Yes", "Yes"),
            ("No", "No"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(_photos_count__gt=0)
        elif value == "No":
            return queryset.filter(_photos_count=0)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):  # new option: object permissions
    list_display = ['title', 'slug', 'author', 'photos_count', 'created', 'updated', 'status']
    search_fields = ['title', 'slug', 'author', 'status']
    exclude = ('slug',)

    fieldsets = (
        ('', {
            "fields": ("title",),
        }),
        ('Description', {
            "fields": ("description",),
            "classes": ("grp-collapse grp-closed",)
        }),
        ('Status', {
            "fields": ("status",),
            "classes": ("grp-collapse grp-open",)
        }),
    )
    # readonly_fields = ["slug"]
    list_filter = [HasPhotosFilter]
    inlines = (PhotoInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_photos_count=Count("photos"))
        return queryset

    def photos_count(self, obj):
        return obj._photos_count


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['title'].disabled = True
            form.base_fields['author'].disabled = True
        return form

    photos_count.admin_order_field = "_photos_count"
    photos_count.short_description = "Number of photos"

