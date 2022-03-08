from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .users import views
from .views import (
    CategoriesViewSet, GenresViewSet, TitlesViewSet,
    ReviewViewSet, CommentViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', views.UserViewSet, basename='users')

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')

auth_urls = [
    path(
        'auth/token/', views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/signup/', views.UserSignUpView.as_view(),
        name='sign_up'
    ),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth_urls)),
]
