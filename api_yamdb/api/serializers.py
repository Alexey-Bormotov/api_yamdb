import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (
    Categories, Genres, Titles, GenresTitles,
    Comment, Review,
    )


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Categories.objects.all())]
    )

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Genres.objects.all())]
    )

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False)
    genre = GenresSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        avg_rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']

        return avg_rating

    class Meta:
        model = Titles
        fields = '__all__'


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
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
        if not Categories.objects.filter(slug=value.slug).exists():
            raise serializers.ValidationError(f'Категории {value} не существует.')
        return value

    def validate_genre(self, value):
        for genre in value:
            if not Genres.objects.filter(slug=genre.slug).exists():
                raise serializers.ValidationError(f'Жанра {genre} не существует.')
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')

        title = Titles.objects.create(**validated_data, category=category)

        for genre in genres:
            genre = Genres.objects.get(slug=genre.slug)
            GenresTitles.objects.create(genre=genre, title=title)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)

        category = validated_data.pop('category')
        instance.category = validated_data.get('category', category)

        title = Titles.objects.get(pk=instance.id)
        if 'genre' in validated_data:
            genres = validated_data.pop('genre')
            for genre in genres:
                genre = Genres.objects.get(slug=genre.slug)
                GenresTitles.objects.create(genre=genre, title=title)

        instance.save()

        return instance

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False,)

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    score = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = '__all__'

    def get_score_average(self, obj):
        score = obj.score.all().aggregate(Avg('score')).get('score_avg')
        # score = obj.objects.aggregate(Avg('score')).get('score_avg')
        if score is None:
            return 0
        return int(score)
