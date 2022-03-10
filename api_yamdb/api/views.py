from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Review
from .filters import TitlesFilter
from .mixins import CategoryGenreViewSet, TitleViewSet, ReviewCommentViewSet
from .permissions import AdminOrReadOnlyPermission
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          TitlesCreateUpdateSerializer,
                          CommentSerializer,
                          ReviewSerializer)


class CategoriesViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(TitleViewSet):
    permission_classes = AdminOrReadOnlyPermission,
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlesCreateUpdateSerializer

        return TitlesSerializer

    def get_queryset(self):
        queryset = Title.objects.all()

        if self.action in ['list', 'retrieve']:
            queryset = Title.objects.annotate(rating=Avg('reviews__score'))

        return queryset


class ReviewViewSet(ReviewCommentViewSet):
    serializer_class = ReviewSerializer

    def check_title(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)

        return title

    def get_queryset(self):
        title = self.check_title()
        queryset = title.reviews.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.check_title())


class CommentViewSet(ReviewCommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()

        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
