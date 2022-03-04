from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .permissions import OnlyAuthorPermission


class ReviewCommentViewSet(ModelViewSet):
    permission_classes = OnlyAuthorPermission,
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
