from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles, Review
from .filters import TitlesFilter
from .mixins import CategoryGenreViewSet, ReviewCommentViewSet
from .permissions import AdminOrReadOnlyPermission
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          TitlesCreateUpdateSerializer,
                          CommentSerializer,
                          ReviewSerializer)


class CategoriesViewSet(CategoryGenreViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoryGenreViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete',]
    permission_classes = AdminOrReadOnlyPermission,
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    queryset = Titles.objects.all()

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
