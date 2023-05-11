from django.contrib.auth.models import AbstractUser
from django.db import models

CHOISES = (
    ('User', 'Пользователь'),
    ('Admin', 'Администратор'),
    ('Moderator', 'Модератор')
)


class Category(models.Model):
    name = models.CharField('название', max_length=50)
    slug = models.SlugField('слаг')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('название', max_length=50)
    slug = models.SlugField('слаг')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('название', max_length=50)
    year = models.DateField('год выпуска')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='категория')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   verbose_name='жанр')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class User(AbstractUser):
    bio = models.TextField('биография', blank=True)
    role = models.CharField('роль', max_length=50, choises=CHOISES)


class Review(models.Model):
    text = models.TextField('текст')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='название')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='автор')
    score = models.IntegerField('счет')
    pub_date = models.DateTimeField('дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    text = models.TextField('текст')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='отзыв')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор')
    pub_date = models.DateTimeField('дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:10]
