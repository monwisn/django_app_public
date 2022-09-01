from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user, assign_perm

from .models import Post, Category, Images


class ReadOnlyAdminMixin:

    def has_add_permission(self):
        return False

    def has_change_permission(self):
        return False

    def has_delete_permission(self):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 3
    verbose_name = 'Image'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, ReadOnlyAdminMixin):
    inlines = [
        ImagesInline,
    ]
    list_display = ['title', 'slug', 'author', 'place', 'category', 'created', 'status']
    search_fields = ['title', 'slug', 'description', 'place', 'author']
    list_filter = ['status']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['title'].disabled = True
            form.base_fields['author'].disabled = True
        return form


@admin.register(Category)
class CategoryAdmin(GuardedModelAdmin):    # new option: object permissions
    list_display = ['title', 'description', 'slug', 'created', 'updated']
    search_fields = ['title', 'description']
    exclude = ('slug',)

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        data = self.get_model_objects(request)
        return data

    def get_model_objects(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'edit', 'delete']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'view')

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'change')

    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'delete')
