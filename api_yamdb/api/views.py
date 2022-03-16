import secrets

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from api_yamdb import settings
from reviews.models import Category, Genre, Title, Review
from .filters import TitlesFilter
from .mixins import CategoryGenreViewSet, TitleReviewCommentViewSet
from .permissions import (IsAuthorPermission,
                          IsAdminPermission,
                          IsReadOnlyPermission)
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          TitlesCreateUpdateSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          TokenObtainPairSerializer,
                          UserSerializer,
                          UserSignUpSerializer)


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer


class UserSignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = secrets.token_urlsafe()
        user, _ = get_user_model().objects.get_or_create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email'),
            confirmation_code=token
        )
        message = (f'Для подтверждения регистрации на сайте перейдите, '
                   f'пожалуйста, по ссылке {settings.HOST_NAME}?code={token}')
        send_mail(
            subject='Регистрация на сайте',
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminPermission)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        ['GET', 'PATCH'], permission_classes=(IsAuthenticated,),
        detail=False, url_path='me'
    )
    def me_user(self, request):
        if not request.data:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.user.role == 'admin':
            serializer.update(request.user, serializer.validated_data)
        else:
            serializer.nonadmin_update(
                request.user, serializer.validated_data
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(TitleReviewCommentViewSet):
    permission_classes = [IsReadOnlyPermission | IsAdminPermission]
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


class ReviewViewSet(TitleReviewCommentViewSet):
    permission_classes = IsAuthorPermission,
    pagination_class = PageNumberPagination
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


class CommentViewSet(TitleReviewCommentViewSet):
    permission_classes = IsAuthorPermission,
    pagination_class = PageNumberPagination
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
