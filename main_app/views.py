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
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, VehicleForm
from .models import *
from .api import *


def home(request):
    vehicles = Vehicle.objects.all()
    trips = Trip.objects.all()
    
    try:
        vehicle = Vehicle.objects.first()
    except Vehicle.DoesNotExist:
        vehicle = None

    return render(request, 'home.html', {'vehicles': vehicles, 'trips': trips, 'vehicle': vehicle})

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
        if not self.get_queryset().exists():
            return redirect('vehicle_create')
        
        redirect_url = get_login_redirect()
        return redirect(redirect_url)
    
    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


class CreateVehicle(CreateView):
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
        makes_data.insert(0, {'id': '', 'name': '--- Select Make ---'})

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
            model_data.insert(0, {'id': '', 'name': '--- Select Model ---'})
            context['models'] = model_data if len(model_data) > 1 else []

        # use context to set dropdown options
        context['makes'] = makes_data if len(makes_data) > 0 else []

        return context
    
    def form_valid(self, form):        
        vehicle = form.save(commit=False)

        # get selected model ID
        selected_model = form.cleaned_data.get('model')
        
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
    

class UpdateVehicle(UpdateView):
    model= Vehicle
    fields= ['make', 'model']
    template_name = 'main_app/edit_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateVehicle, self).get_context_data(**kwargs)

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
        makes_data.insert(0, {'id': '', 'name': '--- Select Make ---'})

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
            model_data.insert(0, {'id': '', 'name': '--- Select Model ---'})
            context['models'] = model_data if len(model_data) > 1 else []

        # use context to set dropdown options
        context['makes'] = makes_data if len(makes_data) > 0 else []

        return context

    def form_valid(self, form):
        vehicle = form.save(commit=False)

        # get selected model ID
        selected_model = form.cleaned_data.get('model')
        
        # fetch estimate for specified vehicle
        estimate = get_estimate(selected_model)

        # update data for model creation
        vehicle.make = estimate['data']['attributes']['vehicle_make']
        vehicle.model = estimate['data']['attributes']['vehicle_model']
        vehicle.year = estimate['data']['attributes']['vehicle_year']
        vehicle.carbon = estimate['data']['attributes']['carbon_g'] / 100

        # save data to model
        vehicle.save()

        return super(UpdateVehicle, self).form_valid(form)


def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    vehicle.delete()

    all_vehicles = Vehicle.objects.exclude(id=vehicle_id).order_by('id')

    try:
        new_vehicle = all_vehicles.first()
        return redirect('vehicle_detail', vehicle_id=new_vehicle.id)
    except:
        return redirect('vehicle_create')


def vehicle_detail(request, vehicle_id):
    if not vehicle_id: return redirect(request, 'vehicle_form.html')
    user = request.user.userprofile
    vehicles = Vehicle.objects.all()
    trips = Trip.objects.all()

    vehicle= Vehicle.objects.get(id=vehicle_id)
    return render(request, 'vehicles/detail.html', {'vehicle':vehicle, 'vehicles': vehicles, 'trips': trips, 'output': user.output, 'cost': user.cost})

# ------------------------------------------------------------------------------------------#
class TripList(LoginRequiredMixin, ListView):
    model = Trip
    template_name= 'trips/index.html'

class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['date', 'departure', 'destination', 'distance']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
        
    def get_queryset(self):
        return Trip.objects.filter(vehicle__user = self.request.user)


class CreateTrip(CreateView):
    model = Trip
    form_class = CreateTripForm

    def form_valid(self, form):
        trip = form.save(commit=False)
        

        # set vehicle id reference
        vehicle_id = self.kwargs['vehicle_id']
        form.instance.vehicle_id = vehicle_id
        
        # define vehicle and user
        vehicle = Vehicle.objects.get(id=vehicle_id)
        user = UserProfile.objects.get(user=vehicle.user)
        
        distance = form.cleaned_data['distance']

        pounds = vehicle.carbon / 453.592
        trip.carbon = pounds * distance
        trip.cost = int(trip.carbon / 48)



        # set cost based on distance
        vehicle.mileage += trip.distance
        user.output += trip.carbon / 2204
        user.cost += trip.cost

        user.save()
        vehicle.save()
        trip.save()

        print(user.output, trip.carbon)
        
        return redirect('vehicle_detail', vehicle_id=vehicle_id)

class UpdateTrip(UpdateView):
    model = Trip
    fields = '__all__'

def delete_trip(request, vehicle_id, pk):
    trip = get_object_or_404(Trip, vehicle_id=vehicle_id, pk=pk)
    trip.delete()
    return redirect('vehicle_detail', vehicle_id=vehicle_id)


def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

# ------------------------------------------------------------------------------------------#