from django import forms
from django.views import View
from django.forms.widgets import DateInput
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime
from typing import Any
from .forms import CustomUserCreationForm, VehicleForm
from .models import *
from .api import get_makes
import json
import os
import requests


# API Fns:
# @require_http_methods(["GET", "POST"])
# def add_or_edit_vehicle(request, vehicle_id=None):
#     if vehicle_id:
#         vehicle = Vehicle.objects.get(pk=vehicle_id)
#         form = VehicleForm(request.POST or None, instance=vehicle)
#     else:
#         vehicle = None
#         form = VehicleForm(request.POST or None)
#     
#     if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         make_id = request.GET.get('make_id')
#         if make_id:
#             models = get_models_for_make(make_id)
#             return JsonResponse({'models': models})
# 
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('vehicle_list')  # Redirect to vehicle list or detail view as appropriate
# 
#     # Ensure this part is outside of the 'if' block
#     car_makes = get_makes()  # This will be called on both GET and POST if form is not valid
#     print(car_makes) 
#     context = {
#         'form': form,
#         'car_makes': car_makes,
#         'vehicle_id': vehicle_id,
#     }
# 
#     return render(request, 'add_or_edit_vehicle.html', context)  # Make sure this template exists



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

    # for make in makes:
    #     print(make['data']['id'])
    #     print(make['data']['attributes']['name'])

    # for model in models:
    #     print(model['data']['id'])
    #     print(model['data']['attributes']['name'])
    #     print(model['data']['attributes']['year'])


    return render(request, 'home.html', {'vehicles': vehicles, 'trips': trips, 'vehicle': vehicle})


def google_logout(request):
    logout(request)
    return redirect("/")

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

    response = requests.post(api_url, data=json_data, headers=headers)

    if response.status_code == 201:
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



class CreateVehicle(LoginRequiredMixin, CreateView):
    model = Vehicle
    fields = ['make', 'model']

    def get_context_data(self, **kwargs):
        context = super(CreateVehicle, self).get_context_data(**kwargs)
        
        # fetch make data
        makes_response = get_makes()

        # build and sort makes list
        makes_data = [
            {
                'id': item['data']['id'], 
                'name': item['data']['attributes']['name']
            } 
            for item in makes_response
        ]
        makes_data = sorted(makes_data, key=lambda x: x['name'])

        # get make query param if make selected
        selected_make = self.request.GET.get('make')

        # fetch models and update models dropdown
        if selected_make:
            models_response = get_models(selected_make)
            model_data = [
                {
                    'id': item['data']['id'], 
                    'name': item['data']['attributes']['name'],
                    'year': item['data']['attributes']['year']
                } 
                for item in models_response
            ]

            model_data = sorted(model_data, key=lambda x: x['name'])
            context['models'] = model_data if len(model_data) > 0 else []

        # use context to set dropdown options
        context['makes'] = makes_data if len(makes_data) > 0 else []

        return context
    
    def form_valid(self, form):        
        vehicle = form.save(commit=False)

        # get selected model ID
        selected_model = form.cleaned_data.get('model')
        
        # {"data":{
        #         "id":"fe61a2be-a69f-4016-b2a0-3203433d0afc",
        #         "type":"estimate",
        #         "attributes":{
        #             "distance_value":100.0,
        #             "vehicle_make":"Infiniti",
        #             "vehicle_model":"FX35 AWD",
        #             "vehicle_year":2003,
        #             "vehicle_model_id":"c7ea1f8d-b6bf-4618-9bd2-88c12313c171",
        #             "distance_unit":"mi",
        #             "estimated_at":"2024-01-17T16:11:20.476Z",
        #             "carbon_g":52276,
        #             "carbon_lb":115.25,
        #             "carbon_kg":52.28,
        #             "carbon_mt":0.05
        #         }
        #     }
        # }
        
        # fetch estimate for specified vehicle
        estimate = get_estimate(selected_model)

        # update data for model creation
        vehicle.make = estimate['data']['attributes']['vehicle_make']
        vehicle.model = estimate['data']['attributes']['vehicle_model']
        vehicle.year = estimate['data']['attributes']['vehicle_year']
        vehicle.fuel = 'R'
        vehicle.carbon = estimate['data']['attributes']['carbon_g'] / 100
        vehicle.user = self.request.user

        # save data to model
        vehicle.save()

        return super(CreateVehicle, self).form_valid(form)
    
    

class UpdateVehicle(LoginRequiredMixin, UpdateView):
    model= Vehicle
    fields='__all__'

class DeleteVehicle(LoginRequiredMixin, DeleteView):
    model = Vehicle
    success_url = '/'

@login_required
def vehicle_detail( request, vehicle_id):
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


class CreateTrip(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = CreateTripForm

    def form_valid(self, form):
        vehicle_id = self.kwargs['vehicle_id']
        form.instance.vehicle_id = vehicle_id
        form.save()

        return redirect('vehicle_detail', vehicle_id=vehicle_id)

class UpdateTrip(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = '__all__'

# class DeleteTrip(DeleteView):
#     model=Trip
#     success_url = '/'

@login_required
def delete_trip(request, vehicle_id, pk):
    trip = get_object_or_404(Trip, vehicle_id=vehicle_id, pk=pk)
    trip.delete()
    return redirect('vehicle_detail', vehicle_id=vehicle_id)

@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

# ------------------------------------------------------------------------------------------#
class GeocodingView(ListView):