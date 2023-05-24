from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Category, Comment, Genre, Review, Title, User


class GenreInline(admin.TabularInline):

    model = Title.genre.through
    raw_id_fields = ('genre', )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'pk',
        'year',
        'description',
        'category',
        'get_genres'
    )
    list_editable = ('category',)
    search_fields = ('name', 'year',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'
    inlines = [GenreInline]

    @admin.display(description='Жанры')
    def get_genres(self, obj):
        return [genre.name for genre in obj.genre.all()]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'pk',
        'slug'
    )
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'bio'
    )
    list_editable = ('role',)
    search_fields = ('username', 'email',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(Review)
admin.site.register(Comment)
admin.site.unregister(Group)
