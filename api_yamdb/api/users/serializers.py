import os
import secrets

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user = get_object_or_404(
            get_user_model(), username=attrs.get('username')
        )
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                'Некорректный код подтверждения'
            )
        data = {}
        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

    def validate(self, attrs):
        super().validate(attrs)
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Некорректное имя пользователя'
            )
        return attrs

    def create(self, validated_data):
        token = secrets.token_urlsafe()
        user = get_user_model().objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            confirmation_code=token
        )
        message = (f'Для подтверждения регистрации на сайте перейдите, '
                   f'пожалуйста, по ссылке '
                   f'{os.getenv("HOST_NAME", "mysite.com/")}'
                   f'?code={token}')
        send_mail(
            subject='Регистрация на сайте',
            message=message,
            from_email='info@mail.com',
            recipient_list=[user.email]
        )
        return validated_data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def nonadmin_update(self, instance, validated_data):
        validated_data.pop('role', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
