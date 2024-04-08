from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from vibestock.utils.models.base import BaseModel
from vibestock.users.managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={'unique': 'There is already a user with that email registered.'}
    )
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
