from django.db import models
from django.contrib.auth.models import AbstractUser

from reports.models import FinanceReport

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField('email adress', unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email