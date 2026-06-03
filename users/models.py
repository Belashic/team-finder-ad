from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from team_finder.constants import (
    AVATAR_UPLOAD_DIR,
    USER_ABOUT_MAX_LENGTH,
    USER_FIRST_NAME_MAX_LENGTH,
    USER_LAST_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
)

from .managers import UserManager
from .utils import generate_avatar


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=USER_FIRST_NAME_MAX_LENGTH, verbose_name='Имя')
    last_name = models.CharField(max_length=USER_LAST_NAME_MAX_LENGTH, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to=AVATAR_UPLOAD_DIR, blank=True, verbose_name='Аватар')

    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH,
        blank=True,
        unique=True,
        default='',
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message='Телефон должен быть в формате +7XXXXXXXXXX'
            )
        ],
        verbose_name='Телефон'
    )

    github_url = models.URLField(blank=True, verbose_name='GitHub')
    about = models.TextField(max_length=USER_ABOUT_MAX_LENGTH, blank=True, verbose_name='О себе')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Избранные проекты',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            initial_letter = self.first_name[0].upper() if self.first_name else 'U'
            self.avatar = generate_avatar(initial_letter)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'