from django.db import models
from django.urls import reverse


FUEL = (('P', 'Premium'), ('R', 'Regular'), ('M', 'Mid-Grade'))
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    



class Vehicle (models.Model):
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.IntegerField()
    fuel = models.CharField(max_length=1, choices= FUEL, default = FUEL[1][0])
    carbon = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __Str__(self):
        return  f'You have assigned {self.get_fuel_display()} for your {self.make} {self.model} {self.year} '

    def get_absolute_url(self):
        return reverse('vehicle_detail', kwargs={'vehicle_id': self.id})


class Trip(models.Model):
    date = models.DateField()
    departure= models.TextField(max_length=255)
    destination= models.TextField(max_length=255)
    co_em= models.IntegerField()
    distance= models.IntegerField() 
    vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Trip ID: {self.id} - Trip Date: {self.date}'

    def get_absolute_url(self):
        return reverse('trip_detail', kwargs={'trip_id': self.id})
    

    class Meta:
        ordering = ['-date']