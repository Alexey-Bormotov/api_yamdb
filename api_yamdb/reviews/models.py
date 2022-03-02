from django.db import models


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
        return f'Категория {self.name}'


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
        return f'Жанр {self.name}'


class Titles(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год издания произведения',
    )
    rating = models.IntegerField(
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
        return f'Произведение {self.name}'


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre}'
