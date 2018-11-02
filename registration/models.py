from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
	email = models.EmailField(unique=True)

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]
