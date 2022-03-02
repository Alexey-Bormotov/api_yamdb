from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genres, Titles
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer)


class CategoriesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    # permission_classes = [IsAdminOrReadOnly,]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'titles_c__slug', 'titles_g__slug')
