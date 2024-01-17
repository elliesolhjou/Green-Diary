import json
import os
from django import forms
from datetime import datetime
from django.forms.widgets import DateInput
from typing import Any
from django.db.models.query import QuerySet
import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, VehicleForm
from .models import *
from .api import get_makes


# API Fns:
def add_or_edit_vehicle(request, vehicle_id=None):
    if vehicle_id:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        form = VehicleForm(request.POST or None, instance=vehicle)
    else:
        vehicle = None
        form = VehicleForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('vehicle_list')  # Redirect to vehicle list or detail view as appropriate

    # Ensure this part is outside of the 'if' block
    car_makes = get_makes()  # This will be called on both GET and POST if form is not valid
    context = {
        'form': form,
        'car_makes': car_makes,
        'vehicle_id': vehicle_id,
    }
    return render(request, 'add_or_edit_vehicle.html', context)  # Make sure this template exists





# Create your views here.

def home(request):
    vehicles = Vehicle.objects.all()
    trips = Trip.objects.all()
    
    try:
        vehicle = Vehicle.objects.first()
    except Vehicle.DoesNotExist:
        vehicle = None

    for trip in trips:
        pounds = 300 / 453.592
        trip.output = int(trip.distance * pounds)
        trip.cost = int(trip.output / 48)

    makes = get_makes()
    models = get_models('1a51451b-c27e-4e24-92f5-2432ca359a41')
    estimate = get_estimate('e16aa48e-4b94-441d-87a0-b12baf385cec')

    # for make in makes:
    #     print(make['data']['id'])
    #     print(make['data']['attributes']['name'])

    # for model in models:
    #     print(model['data']['id'])
    #     print(model['data']['attributes']['name'])
    #     print(model['data']['attributes']['year'])

    print(estimate)


    return render(request, 'home.html', {'vehicles': vehicles, 'trips': trips, 'vehicle': vehicle})




def get_makes():
    api_url = 'https://www.carboninterface.com/api/v1/vehicle_makes'
    headers = {
        'Authorization': 'Bearer sjXOxFgqEqHpfHKwvIclAg'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_models(make_id):
    api_url = f'https://www.carboninterface.com/api/v1/vehicle_makes/{make_id}/vehicle_models'
    headers = {
        'Authorization': 'Bearer sjXOxFgqEqHpfHKwvIclAg'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_estimate(vehicle_id):
    api_url = 'https://www.carboninterface.com/api/v1/estimates'
    headers = {
        'Authorization': 'Bearer sjXOxFgqEqHpfHKwvIclAg',
        'Content-Type': 'application/json'
    }

    data = {
        "type": "vehicle",
        "distance_unit": "mi",
        "distance_value": 100,
        "vehicle_model_id": vehicle_id
    }
    
    json_data = json.dumps(data)

    response = requests.get(api_url, data=json_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")



# ------------------------------------------------------------------------------------------#
                                            # CBV 
# ------------------------------------------------------------------------------------------#
    
class UpdateUser(UpdateView):
    model = User
    fields = '__all__'

class DeleteUser(DeleteView):
    model=User
    success_url  = '/'


def signup(request):
    error_message= ""
    if request.method =='POST':
        # create a form with info passed in through Req.Post
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # create new user if form is valid
            user = form.save()
            login(request, user)
            return redirect("vehicle_create")
        else:
            print(form.errors)
            error_message= " Invalid. Please try again!"
    # clear form after user creation
    form = CustomUserCreationForm
    # pass data to html to display
    context = {'form': form, 'error_message': error_message}
    return render (request, 'registration/signup.html', context)


def get_login_redirect():
    try:
        default_vehicle = Vehicle.objects.first()
        if default_vehicle:
            return reverse('vehicle_detail', args=[default_vehicle.id])
    except Vehicle.DoesNotExist:
        pass 

    return '/' 

# ------------------------------------------------------------------------------------------#
class VehicleList(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/index.html'

    def dispatch(self, request, *args, **kwargs):
        redirect_url = get_login_redirect()
        return redirect(redirect_url)
    
    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields=['make', 'model', 'year', 'fuel']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class CreateVehicle(CreateView):
    model = Vehicle
    form_class = CreateVehicleForm
    # makes = get_makes()

    def get_success_url(self):
        vehicle = self.object
        return reverse('vehicle_detail', kwargs={'vehicle_id': vehicle.id})
    
    def get_queryset(self):
        return Vehicle.objects.filter(vehicle__user = self.request.user)
    
class UpdateVehicle(UpdateView):
    model= Vehicle
    fields='__all__'

class DeleteVehicle(DeleteView):
    model = Vehicle
    success_url = '/'


def vehicle_detail(request, vehicle_id):
    vehicles = Vehicle.objects.all()
    trips = Trip.objects.all()

    for trip in trips:
        print(trip.vehicle_id)

    vehicle= Vehicle.objects.get(id=vehicle_id)
    return render(request, 'vehicles/detail.html', {'vehicle':vehicle, 'vehicles': vehicles, 'trips': trips})

# ------------------------------------------------------------------------------------------#
class TripList(LoginRequiredMixin, ListView):
    model = Trip
    template_name= 'trips/index.html'

class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['date', 'departure', 'destination', 'co_em', 'distance']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
        
    def get_queryset(self):
        return Trip.objects.filter(vehicle__user = self.request.user)


class CreateTrip(CreateView):
    model = Trip
    form_class = CreateTripForm

    def form_valid(self, form):
        vehicle_id = self.kwargs['vehicle_id']
        form.instance.vehicle_id = vehicle_id
        form.save()

        return redirect('vehicle_detail', vehicle_id=vehicle_id)

class UpdateTrip(UpdateView):
    model = Trip
    fields = '__all__'

# class DeleteTrip(DeleteView):
#     model=Trip
#     success_url = '/'

def delete_trip(request, vehicle_id, pk):
    trip = get_object_or_404(Trip, vehicle_id=vehicle_id, pk=pk)
    trip.delete()
    return redirect('vehicle_detail', vehicle_id=vehicle_id)


def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

# ------------------------------------------------------------------------------------------#