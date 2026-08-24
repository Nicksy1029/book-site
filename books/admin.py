from django.contrib import admin
from .models import Genre, Book

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'downloads_count', 'created_at')
    list_filter = ('is_approved', 'genres', 'created_at')
    search_fields = ('title', 'author__username')

    list_editable = ('is_approved',)