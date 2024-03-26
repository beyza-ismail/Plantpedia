from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('a', 'Admin'),
        ('u', 'User')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, )


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Plant(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    scientific_name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)  # go nema vo ER diagram
    age = models.IntegerField(default=0)  # go nema vo ER diagram
    description = models.TextField()
    care_instructions = models.TextField()
    image = models.ImageField(upload_to="data/")

    def __str__(self):
        return f"{self.name}"

class Review(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField(default=0)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return f"For: {self.plant}, by: {self.user}"