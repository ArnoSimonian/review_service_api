from django.db import models


class Genre_Category_Abstract(models.Model):
    """Абстрактная модель для Категорий и Жанров"""

    name = models.CharField('название', max_length=256)
    slug = models.SlugField('слаг', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.slug
