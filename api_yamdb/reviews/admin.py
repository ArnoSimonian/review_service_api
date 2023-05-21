from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


class GenreInline(admin.TabularInline):

    model = Title.genre.through
    raw_id_fields = ("genre", )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genres'
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'
    inlines = [GenreInline]

    @admin.display(description='genres')
    def get_genres(self, obj):
        return [genre.name for genre in obj.genre.all()]


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
