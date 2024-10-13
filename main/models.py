from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    address = models.TextField()


    day = models.DateField(null=True)
    number_of_people = models.IntegerField(default=0)

    watering_garden = models.CharField(max_length=255, default='')
    cooking = models.CharField(max_length=255, default='')
    dishwashing = models.CharField(max_length=255, default='')
    laundry = models.CharField(max_length=255, default='')
    showers = models.CharField(max_length=255, default='')
    toilet_flush = models.CharField(max_length=255, default='')

    total = models.TextField(default='')
    total_daily = models.TextField(default='')
    #
    # def __str__(self):
    #     return self.user
