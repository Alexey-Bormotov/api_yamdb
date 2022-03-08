import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (
    Category, Genre, Title, GenreTitle,
    Comment, Review)


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False)
    genre = GenresSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        avg_rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']

        return avg_rating

    class Meta:
        model = Title
        fields = '__all__'


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год издания.')
        return value

    def validate_category(self, value):
        if not Category.objects.filter(slug=value.slug).exists():
            raise serializers.ValidationError(
                f'Категории {value} не существует.')
        return value

    def validate_genre(self, value):
        for genre in value:
            if not Genre.objects.filter(slug=genre.slug).exists():
                raise serializers.ValidationError(
                    f'Жанра {genre} не существует.')
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data, category=category)

        for genre in genres:
            genre = Genre.objects.get(slug=genre.slug)
            GenreTitle.objects.create(genre=genre, title=title)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description)

        category = validated_data.pop('category')
        instance.category = validated_data.get('category', category)

        title = Title.objects.get(pk=instance.id)
        if 'genre' in validated_data:
            genres = validated_data.pop('genre')
            for genre in genres:
                genre = Genre.objects.get(slug=genre.slug)
                GenreTitle.objects.create(genre=genre, title=title)

        instance.save()

        return instance

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        exclude = ('review',)
