from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from blogs.models import Author, Category,Tag,Blog
from shared.admin import MyTranslationOption


@admin.register(Author)
class AuthorAdmin(MyTranslationOption):
    list_display = ['id','full_name','is_active','created_at']
    search_fields = ['full_name','professions']
    list_filter = ['created_at','professions','is_active','updated_at']


@admin.register(Category)
class CategoryAdmin(MyTranslationOption):
    list_display = ['id','title','is_active','created_at']
    search_fields = ['title']
    list_filter = ['created_at','is_active','updated_at']

@admin.register(Tag)
class TagAdmin(MyTranslationOption):
    list_display = ['id','title','is_active','created_at']
    search_fields = ['title']
    list_filter = ['created_at','is_active','updated_at']

@admin.register(Blog)
class BlogAdmin(MyTranslationOption):
    list_display = ['id','title','is_active','created_at']
    search_fields = ['title']
    list_filter = ['authors','categories','tags', 'created_at','is_active','updated_at']

