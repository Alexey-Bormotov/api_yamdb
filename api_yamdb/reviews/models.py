from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return f'{self.name}'


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return f'{self.name}'


class Titles(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год издания произведения',
    )
    rating = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Рейтинг произведения',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
    )
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        through='GenresTitles',
        verbose_name='Жанры произведения',
        related_name='titles_g',
    )
    category = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        related_name='titles_c',
    )

    def __str__(self):
        return f'{self.name}'


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre}'

class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.SECASCADET_NULL,
        related_name='title',
        verbose_name='название произведения',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации обзора', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    def __str__(self):
        return self.author + '_' + self.text[:10]