from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles, Review
from .mixins import CategoryGenreTitleViewSet, ReviewCommentViewSet
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          TitlesCreateUpdateSerializer,
                          CommentSerializer,
                          ReviewSerializer)


class CategoriesViewSet(CategoryGenreTitleViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    lookup_field = 'slug'


class GenresViewSet(CategoryGenreTitleViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

    lookup_field = 'slug'


class TitlesViewSet(CategoryGenreTitleViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete',]
    # Как то можно добавить патч, а не переопределять атрибут?
    queryset = Titles.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre')
    # Жанры и категории пока фильтрует только по id. Может быть нужен FilterSet?

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlesCreateUpdateSerializer
        return TitlesSerializer

class ReviewViewSet(ReviewCommentViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(ReviewCommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)
