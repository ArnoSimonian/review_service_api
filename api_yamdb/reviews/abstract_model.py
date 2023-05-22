from django.db import models

from api.utils import NAME_LENGTH, SLUG_LENGTH


class GenreCategoryAbstract(models.Model):
    """Абстрактная модель для Категорий и Жанров"""

    name = models.CharField(verbose_name='название', max_length=NAME_LENGTH)
    slug = models.SlugField(verbose_name='слаг', max_length=SLUG_LENGTH, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.slug
