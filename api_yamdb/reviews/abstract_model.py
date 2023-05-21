from django.db import models


class GenreCategoryAbstract(models.Model):
    """Абстрактная модель для Категорий и Жанров"""

    name = models.CharField(verbose_name='название', max_length=256)
    slug = models.SlugField(verbose_name='слаг', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.slug
