
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    full_name = models.CharField(max_length=128, default='')
    car = models.CharField(max_length=64, default='')
    is_expert = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'car']

    def __str__(self):
        return self.email

class DiagnosticRequest(models.Model):
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
