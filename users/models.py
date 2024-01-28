from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfile(models.Model):
    # uses built-in user model 
    timestamp = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(verbose_name = "Address", max_length = 100, null=True, blank = True)
    city = models.CharField(verbose_name = "City", max_length = 100, null=True, blank = True)
    state = models.CharField(verbose_name = "State", max_length = 100, null=True, blank = True)
    zip_code = models.CharField(verbose_name = "Zipcode", max_length = 100, null=True, blank = True)
    country = models.CharField(verbose_name = "Country", max_length = 100, null=True, blank = True)
    longitude = models.CharField(verbose_name = "Longitude", max_length = 100, null=True, blank = True)
    latitude = models.CharField(verbose_name = "Latitude", max_length = 100, null=True, blank = True)

    captcha_score = models.FloatField(default = 0.0)