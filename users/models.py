from django.contrib.auth.models import AbstractUser

# from app.models import User

MAX_LENGTH = 80


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username
