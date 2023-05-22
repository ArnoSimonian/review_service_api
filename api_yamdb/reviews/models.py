import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.db import models

from .abstract_model import GenreCategoryAbstract
from .validators import validate_name


class Category(GenreCategoryAbstract):

    class Meta(GenreCategoryAbstract.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_category_slug'
            )
        ]


class Genre(GenreCategoryAbstract):

    class Meta(GenreCategoryAbstract.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_genre_slug'
            )
        ]


class Title(models.Model):
    name = models.CharField(verbose_name='название', max_length=256)
    year = models.PositiveSmallIntegerField(verbose_name='год выпуска',
                                            db_index=True,
                                            validators=[
                                                MaxValueValidator(
                                                dt.date.today().year)
                                            ])
    description = models.TextField(verbose_name='описание',
                                   blank=True)
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='категория')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   verbose_name='жанр')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              verbose_name='жанр',
                              on_delete=models.CASCADE)
    title = models.ForeignKey(Title,
                              verbose_name='произведение',
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр-произведение'

    def __str__(self):
        return f'{self.genre} {self.title}'


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(verbose_name='имя пользователя',
                                max_length=150,
                                unique=True,
                                validators=[validate_name])
    email = models.EmailField(verbose_name='email', max_length=254, unique=True)
    role = models.CharField(
        verbose_name='роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    first_name = models.CharField(verbose_name='имя', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='фамилия', max_length=150, blank=True)
    bio = models.TextField(verbose_name='биография', blank=True)
    confirmation_code = models.CharField(verbose_name='код подтверждения',
                                         max_length=4)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('-username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


class AbstractReviewComment(models.Model):
    """Абстрактная модель для Отзывов и Комментариев"""

    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='автор')
    pub_date = models.DateTimeField(verbose_name='дата публикации',
                                    auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]


class Review(AbstractReviewComment):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='произведение')
    score = models.PositiveSmallIntegerField(verbose_name='оценка',
                                             validators=[
                                                 MinValueValidator(1),
                                                 MaxValueValidator(10)
                                             ])

    class Meta(AbstractReviewComment.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(AbstractReviewComment):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='отзыв')

    class Meta(AbstractReviewComment.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'
