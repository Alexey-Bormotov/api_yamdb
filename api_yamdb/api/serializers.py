from django.db.models import Avg
from rest_framework import serializers

from reviews.models import (
    Categories, Genres, Titles,
    Comment, Review,
    )


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        model = Titles
        fields = '__all__'


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
