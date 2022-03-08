from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .permissions import OnlyAuthorPermission, AdminOrReadOnlyPermission


class CategoryGenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = AdminOrReadOnlyPermission,
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewCommentViewSet(ModelViewSet):
    permission_classes = OnlyAuthorPermission,
    pagination_class = PageNumberPagination
