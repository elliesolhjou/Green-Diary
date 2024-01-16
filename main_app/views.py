import json
import os
from django import forms
from datetime import datetime
from django.forms.widgets import DateInput
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from .models import *
# Create your views here.

def home(request):
    vehicles = Vehicle.objects.all()
    trips = Trip.objects.all()
    user = User.objects.get(pk=1)


    

    for trip in trips:
        pounds = 300 / 453.592
        trip.output = int(trip.distance * pounds)
        trip.cost = int(trip.output / 48)

    return render(request, 'home.html', {'vehicles': vehicles, 'trips': trips})


### DATA TESTING ###
# from django.conf import settings 
# def home(request):
#     vehicles_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/vehicles.json')
#     trips_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/trips.json')
# 
# 
#     with open(trips_path, 'r') as json_data:
#         trip_raw = json.load(json_data)
# 
#     def trip_remap(trip):
#         print(trip)
#         year = trip['startDate'].split('-')[0]
#         date_obj = datetime.strptime(trip['startDate'], '%Y-%m-%d')
#         start = date_obj.strftime('%B, %d')
#         year = trip['endDate'].split('-')[0]
#         date_obj = datetime.strptime(trip['endDate'], '%Y-%m-%d')
#         end = date_obj.strftime('%B, %d')
# 
#         return {
#             'year': year,
#             'start': start,
#             'end': end,
#             'distance': trip['distance'],
#             'weight': trip['impactData']['weight_lb'],
#             'trees': trip['impactData']['trees']
#         }
# 
#     trip_data = [trip_remap(trip) for trip in trip_raw['records']]
# 
#     with open(vehicles_path, 'r') as json_data:
#         vehicle_data = json.load(json_data)
# 
#     return render(request, 'home.html', {'vehicles': vehicle_data, 'trips': trip_data})


# ------------------------------------------------------------------------------------------#
                                            # CBV 
# ------------------------------------------------------------------------------------------#
class CreateUser(CreateView):
    model = User
    fields = '__all__'
    
class UpdateUser(UpdateView):
    model = User
    fields = '__all__'

class DeleteUser(DeleteView):
    model=User
    success_url  = '/'


def user(request):
    user = User.objects.all()
    return render(request, 'users/index.html', {'user':user})



# ------------------------------------------------------------------------------------------#
class VehicleList(ListView):
    model = Vehicle
    template_name = 'vehicles/index.html'


class CreateVehicle(CreateView):
    model = Vehicle
    fields=['make', 'model', 'year', 'fuel']

class UpdateVehicle(UpdateView):
    model= Vehicle
    fields='__all__'

class DeleteVehicle(DeleteView):
    model = Vehicle
    success_url = '/'


def vehicle_detail(request, vehicle_id):
    vehicle= Vehicle.objects.get(id=vehicle_id)
    return render(request, 'vehicles/detail.html', {'vehicle':vehicle})

# ------------------------------------------------------------------------------------------#
class TripList(ListView):
    model = Trip
    template_name= 'trips/index.html'

class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['date', 'departure', 'destination', 'co_em', 'distance']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class CreateTrip(CreateView):
    model = Trip
    form_class = CreateTripForm
    success_url = '/'

class UpdateTrip(UpdateView):
    model = Trip
    fields = '__all__'

# class DeleteTrip(DeleteView):
#     model=Trip
#     success_url = '/'

def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    trip.delete()
    return redirect('/') 


def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

# ------------------------------------------------------------------------------------------#