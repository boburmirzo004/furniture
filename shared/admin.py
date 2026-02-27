from django.contrib import admin

from shared.models import AboutUs


@admin.register(AboutUs)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name','profession','created_at']
    search_fields = ['name','profession','info']
    list_filter = ['profession','created_at','updated_at']

