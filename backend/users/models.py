from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROlE_CHOICES = (
        ("USER", "User"),
        ("ADMIN", "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROlE_CHOICES, default="USER")
