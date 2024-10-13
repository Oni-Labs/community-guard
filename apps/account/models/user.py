import os

from django.contrib.auth.models import AbstractUser
from django.db import models


def path_user_profile_photo(instance, filename) -> str:
    return '/'.join('profile_photo', 
                     str(instance.uuid))


class User(AbstractUser):
    # managers

    # fields
    profile_photo = models.ImageField(
        upload_to=path_user_profile_photo,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.username}'

