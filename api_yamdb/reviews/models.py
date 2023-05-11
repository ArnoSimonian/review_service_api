from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('User', 'Пользователь'),
    ('Admin', 'Администратор'),
    ('Moderator', 'Модератор')
)


class Category(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField('слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField('слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.IntegerField('год выпуска')
    description = models.TextField('Описание',
                                   blank=True)
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='категория')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class User(AbstractUser):
    username = models.CharField('имя пользователя',
                                max_length=150,
                                unique=True)
    email = models.CharField('почта', max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField('биография', blank=True)
    role = models.CharField('роль',
                            max_length=50,
                            choices=CHOICES,
                            default='User',
                            )


class Review(models.Model):
    text = models.TextField('текст')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='произведение')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='автор')
    score = models.IntegerField('оценка')
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
