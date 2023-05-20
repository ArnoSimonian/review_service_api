from django.contrib import admin

from .models import Category, Genre, Review, Title, User, Comment, GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category'
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'



admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(GenreTitle)

