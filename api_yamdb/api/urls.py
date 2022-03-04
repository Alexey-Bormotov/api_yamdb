from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet, GenresViewSet, TitlesViewSet,
    ReviewViewSet, CommentViewSet
    )


router_v1 = DefaultRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)

router_v1.register('reviews', ReviewViewSet,)
router_v1.register(r'reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comment')
router_v1.register(r'reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
