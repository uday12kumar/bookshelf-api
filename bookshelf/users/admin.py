from django.contrib import admin
from .models import User, Author, UserToken


class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_display = ('email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


admin.site.register(Author, AuthorAdmin)