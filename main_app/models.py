from django.db import models

# Create your models here.
class Trip(models.Model):
    date = models.DateField()
    departure= models.TextField(max_length=255)
    destination= models.TextField(max_length=255)
    co_em= models.IntegerField()
    distance= models.IntegerField()
    # vehicle_id

    def __str__(self):
        return self.date
    

class User(models.Model):
    auth_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    # profile

    def __str__(self):
        return self.date



class Vehicle (models.Model):
    vehicle_id = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.IntegerField()
    fuel = models.CharField(max_length=100)
    # MPG
    # carbon

