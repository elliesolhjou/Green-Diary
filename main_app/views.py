import json
import os
from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from .models import *
# Create your views here.
# def home(request):
#     return render(request, 'home.html')


### DATA TESTING ###
from django.conf import settings 
def home(request):
    vehicles_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/vehicles.json')
    trips_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/trips.json')


    with open(trips_path, 'r') as json_data:
        trip_raw = json.load(json_data)

    def trip_remap(trip):
        print(trip)
        year = trip['startDate'].split('-')[0]
        date_obj = datetime.strptime(trip['startDate'], '%Y-%m-%d')
        start = date_obj.strftime('%B, %d')
        year = trip['endDate'].split('-')[0]
        date_obj = datetime.strptime(trip['endDate'], '%Y-%m-%d')
        end = date_obj.strftime('%B, %d')

        return {
            'year': year,
            'start': start,
            'end': end,
            'distance': trip['distance'],
            'weight': trip['impactData']['weight_lb'],
            'trees': trip['impactData']['trees']
        }

    trip_data = [trip_remap(trip) for trip in trip_raw['records']]

    with open(vehicles_path, 'r') as json_data:
        vehicle_data = json.load(json_data)

    return render(request, 'home.html', {'vehicles': vehicle_data, 'trips': trip_data})


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
    fields=['make', 'model', 'year', 'fuel']

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