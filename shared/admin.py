from django.contrib import admin

from shared.models import AboutUs, Contact


@admin.register(AboutUs)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'profession', 'created_at']
    search_fields = ['name', 'profession', 'info']
    list_filter = ['profession', 'created_at', 'updated_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','full_name', 'email', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'subject', 'text']
    list_filter = ['full_name', 'is_read', 'created_at', 'updated_at']
