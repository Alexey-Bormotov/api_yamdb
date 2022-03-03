from rest_framework import serializers

from reviews.models import Categories, Genres, Titles


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
