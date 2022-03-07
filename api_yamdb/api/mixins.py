from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .permissions import OnlyAuthorPermission, AdminOrReadOnlyPermission


class CategoryGenreTitleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    # permission_classes = AdminOrReadOnlyPermission,
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

class ReviewCommentViewSet(ModelViewSet):
    permission_classes = OnlyAuthorPermission,
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
