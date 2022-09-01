from django.contrib import admin

from .models import UserProfile, NewsletterUser, Newsletter


# admin.site.register(UserProfile)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'location', 'birth_date', 'join_date']


@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'joined']
    search_fields = ['email']
    list_filter = ['joined']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'status', 'created', 'updated']
    search_fields = ['subject']
    list_filter = ['status', 'created']


admin.site.site_header = "Welcome to the Admin site"
admin.site.site_title = "Watering Plants Portal"
admin.site.index_title = "Admin Portal"
