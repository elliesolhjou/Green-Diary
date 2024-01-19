from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


FUEL = (('P', 'Premium'), ('R', 'Regular'), ('M', 'Mid-Grade'))
# Create your models here.

class Vehicle (models.Model):
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.IntegerField(null=True)
    fuel = models.CharField(max_length=1, choices= FUEL, default = FUEL[1][0])
    carbon = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __Str__(self):
        return  f'You have assigned {self.get_fuel_display()} for your {self.make} {self.model} {self.year} '

    def get_absolute_url(self):
        return reverse('vehicle_detail', kwargs={'vehicle_id': self.id})


class Locations(models.Model):
    name = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=500, blank = True, null=True)
    city = models.CharField(max_length=500, blank = True, null=True)
    country = models.CharField(max_length=500, blank = True, null=True)
    address = models.CharField(max_length=500, blank = True, null=True)
    lat = models.CharField(max_length=500, blank = True, null=True)
    lng= models.CharField(max_length=500, blank = True, null=True)
    place_id = models.CharField(max_length=500, blank = True, null=True)
    created_at = models.DateTimeField(auto_now_add =True, blank = True, null=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    date = models.DateField()
    co_em= models.IntegerField()
    distance= models.IntegerField() 
    departure= models.ForeignKey(Locations, related_name='trip_departure', on_delete=models.CASCADE)
    destination= models.ForeignKey(Locations, related_name='trip_destination', on_delete=models.CASCADE)
    vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f'Trip ID: {self.id} - Trip Date: {self.date}'
    
    def get_absolute_url(self):
        return reverse('trip_detail', kwargs={'trip_id': self.id})
    
    class Meta:
        ordering = ['-date']


class Distances(models.Model):
    from_location = models.ForeignKey(Locations, related_name='from_location', on_delete = models.CASCADE)
    to_location = models.ForeignKey(Locations, related_name='to_location', on_delete = models.CASCADE)
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    duration_mins = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add =True, blank = True, null=True)

    def __str__(self):
        return str(self.id)