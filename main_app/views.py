import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from .models import *


# Create your views here.
def home(request):
    return render(request, 'home.html')


# def weather(request, city):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=<your_api_key>'.format(city)
#     response = requests.get(url)
#     data = response.json()
#     return JsonResponse(data)
# ------------------------------------------------------------------------------------------#
                                            # CBV 
# ------------------------------------------------------------------------------------------#
# class CreateUser(CreateView):
#     model = User
#     fields = '__all__'


class UpdateUser(UpdateView):
    model = User
    fields = '__all__'

class DeleteUser(DeleteView):
    model=User
    success_url  = " "


def user(request):
    user = User.objects.all()
    return render(request, 'users/index.html', {'user':user})

# ------------------------------------------------------------------------------------------#
class VehicleList(ListView):
    model = Vehicle
    template_name = 'vehicles/index.html'


class CreateVehicle(CreateView):
    model = Vehicle
    fields='__all__'

class UpdateVehicle(UpdateView):
    model= Vehicle
    fields='__all__'

class DeleteVehicle(DeleteView):
    model = Vehicle
    success_url = ''


def vehicle_detail(request, vehicle_id):
    vehicle= Vehicle.objects.get(id=vehicle_id)
    return render(request, 'vehicles/detail.html', {'vehicle':vehicle})

# ------------------------------------------------------------------------------------------#
class TripList(ListView):
    model = Trip
    template_name= 'trips/index.html'
class CreateTrip(CreateView):
    model = Trip
    fields='__all__'

class UpdateTrip(UpdateView):
    model = Trip
    fields = '__all__'

class DeleteTrip(DeleteView):
    model=Trip
    success_url = ''


def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

# ------------------------------------------------------------------------------------------#