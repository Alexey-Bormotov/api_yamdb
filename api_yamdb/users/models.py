from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as BaseGroup
from django.db import models


class Group(BaseGroup):

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        proxy = True


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    bio = models.TextField(blank=True, verbose_name='О себе')
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default=USER, verbose_name='Роль'
    )
    confirmation_code = models.TextField(
        null=True, verbose_name='Код подтверждения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role:
            if self.role == self.ADMIN:
                self.is_superuser = True
                self.is_staff = True
            if self.role == self.MODERATOR:
                self.is_staff = True
            return super(User, self).save(*args, **kwargs)
        if self.is_superuser:
            self.role = self.ADMIN
        elif self.is_staff:
            self.role = self.MODERATOR
        else:
            self.role = self.USER
        return super(User, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == 'admin'
