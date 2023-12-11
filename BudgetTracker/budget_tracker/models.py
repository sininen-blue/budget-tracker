from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Expense(models.Model):
    category = models.CharField(max_length=50)
    quantity = models.FloatField()
    date = models.DateField(default=now)


class Income(models.Model):
    quantity = models.FloatField()
    date = models.DateField(default=now)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    savings = models.FloatField()

    def __str__(self):
        return self.user.username
