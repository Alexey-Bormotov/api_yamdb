from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from . import serializers as sz
from .. import permissions


class TokenObtainPairView(TokenViewBase):
    serializer_class = sz.TokenObtainPairSerializer


class UserSignUpView(CreateAPIView):
    serializer_class = sz.UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = sz.UserSerializer
    permission_classes = (IsAuthenticated, permissions.IsAdminPermission)
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
