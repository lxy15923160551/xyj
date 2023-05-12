from django.db import models
from django.contrib.auth.models import AbstractUser


class AggregatorUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    real_name = models.CharField(max_length=64)

    def __str__(self):
        return self.usernamea
