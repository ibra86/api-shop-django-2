from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CharField

MAX_LENGTH = 80


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
