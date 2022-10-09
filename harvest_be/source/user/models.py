from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
