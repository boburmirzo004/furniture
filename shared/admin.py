from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from shared.models import AboutUs, Contact


class MyTranslationOption(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(AboutUs)
class AboutAdmin(MyTranslationOption):
    list_display = ['name', 'profession', 'created_at']
    search_fields = ['name', 'profession', 'info']
    list_filter = ['profession', 'created_at', 'updated_at']


@admin.register(Contact)
class ContactAdmin(MyTranslationOption):
    list_display = ['id', 'full_name', 'email', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'subject', 'text']
    list_filter = ['full_name', 'is_read', 'created_at', 'updated_at']
