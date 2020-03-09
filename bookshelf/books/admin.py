from django.contrib import admin

# Register your models here.
from bookshelf.books.models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


admin.site.register(Book, BookAdmin)


class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_active')


admin.site.register(Genre, GenreAdmin)
