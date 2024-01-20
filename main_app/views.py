from django import forms
from django.views import View
from django.forms.widgets import DateInput
from django.db.models.query import QuerySet
from django.db.models import Sum
import requests
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
import googlemaps
from django.conf import settings
from datetime import datetime
from typing import Any
from .forms import *
from .models import *
from .api import get_makes
import json
import os
import requests
from .forms import DistanceForm
from datetime import datetime


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


    return render(request, 'home.html', {'vehicles': vehicles, 'trips': trips, 'vehicle': vehicle})


def google_logout(request):
    logout(request)
    return redirect("/")

def about(request):
    return render(request, 'about.html')

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
        return super(CreateVehicle, self).form_valid(form)
    
    

class UpdateVehicle(LoginRequiredMixin, UpdateView):
    model= Vehicle
    fields='__all__'

class DeleteVehicle(LoginRequiredMixin, DeleteView):
    model = Vehicle
    success_url = '/'
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

        return super(CreateVehicle, self).form_valid(form)
    

class UpdateVehicle(LoginRequiredMixin, UpdateView):
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
    user = request.user.userprofile
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    trips = vehicle.trip_set.all()
    totals = trips.aggregate(total_carbon=Sum('carbon'), total_cost=Sum('cost'))
    
    total_carbon = totals.get('total_carbon', 0) or 0
    total_cost = totals.get('total_cost', 0) or 0

    user.output -= total_carbon / 2204
    user.cost -= total_cost

    user.save()
    vehicle.delete()

    all_vehicles = Vehicle.objects.filter(user=vehicle.user).exclude(id=vehicle_id).order_by('id')

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

# class CreateTripForm(forms.ModelForm):
#     class Meta:
#         model = Trip
#         fields = ['date', 'departure', 'destination']
#         widgets = {
#             'date': DateInput(attrs={'type': 'date'}),
#         }
        
#     def get_queryset(self):
#         return Trip.objects.filter(vehicle__user = self.request.user)

# class CreateTrip(LoginRequiredMixin, CreateView):
#     model = Trip
#     form_class = CreateTripForm

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

class UpdateTrip(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = '__all__'

@login_required
def delete_trip(request, vehicle_id, pk):
    user = request.user.userprofile
    trip = get_object_or_404(Trip, vehicle_id=vehicle_id, pk=pk)
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    vehicle.mileage -= trip.distance
    user.output -= trip.carbon / 2204
    user.cost -= trip.cost

    vehicle.save()
    user.save()
    trip.delete()

    return redirect('vehicle_detail', vehicle_id=vehicle_id)

@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

# ------------------------------------------------------------------------------------------#
class GeocodingView(View):
    template_name = 'geocoding.html'

    def get(self, request, pk):
        location = Locations.objects.get(pk=pk)
        result = None
        if location.lng and location.lat and location.place_id != None:
            lat = location.lat
            lng = location.lng
            place_id= location.place_id
            label = "from my db"
        
        elif location.address and location.country and location.zipcode and location.city!=None:
            address_string = str(location.address)+", "+ str(location.zipcode)+", "+str(location.city)+", "+str(location.country)
            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            result = gmaps.geocode(address_string)[0]
            lat = result.get('geometry', {}).get('location', {}).get('lat', None)
            lng = result.get('geometry', {}).get('location', {}).get('lng', None)
            place_id = result.get('place_id', {})
            label = "from my API call"

            # lat = location1.get('lat', None)
            # lng = location1.get('lng', None)

            # geometry = result.get('geometry', {})
            # location1 = geometry.get('location', {})

            # saving to DB
            location.lat = lat
            location.lng = lng
            location.place_id = place_id
            location.save()
            

        else:
            result = ""
            lat =""
            lng=""
            place_id = ""
            label = "no call made"
        # to pass data to template:
        context = {
            'location':location,
            'result' : result,
            'lat': lat,
            'lng':lng,
            'place_id': place_id,
            'label': label
        }

        return render(request, self.template_name, context)

class DistanceView(View):
    template_name = 'distance.html'

    def get(self, request):
        form_one = DistanceForm()
        form_two = LocationForm()
        distances = Distances.objects.all()
        locations = Locations.objects.all()
        context = {
            'form_one':form_one,
            'form_two': form_two,
            'distances': distances,
            'locations':locations
        }
        return render(request, self.template_name, context)
    def post(self, request):
        if 'form_one_submit' in request.POST:
            return self.post_form_one(request)
        elif 'form_two_submit' in request.POST:
            return self.post_form_two(request)
        else: 
            return render(request, 'distance.html')
        
    def post_form_one(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            departure_location = form.cleaned_data.get('from_location')
            destination_location = form.cleaned_data.get('to_location')

            # Print statements for debugging
            print("Departure Location:", departure_location)
            print("Destination Location:", destination_location)

            if not departure_location or not destination_location:
                form.add_error(None, "Please select both departure and destination locations.")
            else:
                try:
                    # Initialize Google Maps client
                    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

                    # Get the addresses from the selected locations
                    departure_address = departure_location.address
                    destination_address = destination_location.address

                    # Calculate distance using Google Maps Distance Matrix API
                    distance_result = gmaps.distance_matrix(departure_address, destination_address)
                    distance_info = distance_result['rows'][0]['elements'][0]

                    # Check if the distance calculation was successful
                    if distance_info['status'] == 'OK':
                        distance_meters = distance_info['distance']['value']
                        distance_miles = round(float(distance_meters / 1609.34 ),2) # Convert meters to miles

                        # Create a new instance of the Distances model and save it to the database
                        distance_record = Distances(
                            from_location=departure_location,  # Assign the location instance
                            to_location=destination_location,  # Assign the location instance
                            distance=distance_miles
                        )
                        distance_record.save()

                        # Prepare context with the calculated distance
                        context = {
                            'form': form,
                            'form_two': LocationForm(),
                            'form_one': DistanceForm(),
                            'distance_miles': distance_miles,
                            'departure_location':departure_location,
                            'destination_location':destination_location

                        }

                        # Render a template with the calculated distance
                        return render(request, 'distance.html', context)
                    else:
                        form.add_error(None, "Distance calculation failed.")
                except Exception as e:
                    # Print the exception for debugging
                    print("Error during distance calculation:", e)
                    form.add_error(None, "Distance calculation failed.")
        save_form_one = form.save()

        # Re-render the page with the form (and possibly errors)
        context = {
            'form_one': save_form_one,
            'form_two': LocationForm(),
            'distance_mile':distance_miles,
            'distances': Distances.objects.all(),  
            'locations': Locations.objects.all()
        }
        return render(request, self.template_name, context)
    
    def post_form_two(self,request):
        form_address = LocationForm(request.POST)
        if form_address.is_valid():
            form = form_address.save()
            context = {
            'form_one': DistanceForm(),  # Initialize a new form for distance calculation
            'form_two': LocationForm(),
            'distances': Distances.objects.all(),
            'locations': Locations.objects.all(),

            }
        return render(request, 'distance.html', context)
    

class CreateTrip(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'main_app/trip_form.html'

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_id'] = self.kwargs.get('vehicle_id')
        # Add your additional context here
        context['form_one'] = DistanceForm()
        context['form_two'] = LocationForm()
        context['distances'] = Distances.objects.all()
        context['locations'] = Locations.objects.all()
        context['vehicle_id'] = self.kwargs.get('vehicle_id') 
        # Do not include 'trip_form' as it's added by default
        return context

    def post(self, request, *args, **kwargs):
        if 'form_trip_submit' in request.POST:
            return self.post_form_trip(request)
        elif 'form_one_submit' in request.POST:
            return self.post_form_one(request)
        elif 'form_two_submit' in request.POST:
            return self.post_form_two(request)
        else:
            return super(CreateTrip, self).post(request, *args, **kwargs)
    
    def post_form_trip(self,request):
        form_trip = TripForm(request.POST)
        if form_trip.is_valid():
            form = form_trip.save()
            context = {
            'form':TripForm(),   
            'form_one': DistanceForm(),  # Initialize a new form for distance calculation
            'form_two': LocationForm(),
            'distances': Distances.objects.all(),
            'locations': Locations.objects.all(),

            }
            
        return render(request, self.template_name, context)
        
    def post_form_one(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            departure_location = form.cleaned_data.get('from_location')
            destination_location = form.cleaned_data.get('to_location')

            # Print statements for debugging
            print("Departure Location:", departure_location)
            print("Destination Location:", destination_location)

            if not departure_location or not destination_location:
                form.add_error(None, "Please select both departure and destination locations.")
            else:
                try:
                    # Initialize Google Maps client
                    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

                    # Get the addresses from the selected locations
                    departure_address = departure_location.address
                    destination_address = destination_location.address

                    # Calculate distance using Google Maps Distance Matrix API
                    distance_result = gmaps.distance_matrix(departure_address, destination_address)
                    distance_info = distance_result['rows'][0]['elements'][0]

                    # Check if the distance calculation was successful
                    if distance_info['status'] == 'OK':
                        distance_meters = distance_info['distance']['value']
                        distance_miles = round(float(distance_meters / 1609.34 ),2) # Convert meters to miles

                        # Create a new instance of the Distances model and save it to the database
                        distance_record = Distances(
                            from_location=departure_location,  # Assign the location instance
                            to_location=destination_location,  # Assign the location instance
                            distance=distance_miles
                        )
                        distance_record.save()

                        # Prepare context with the calculated distance
                        context = {
                            'form': TripForm(),
                            'form_two': LocationForm(),
                            'form_one': DistanceForm(),
                            'distance_miles': distance_miles,
                            'departure_location':departure_location,
                            'destination_location':destination_location

                        }

                        # Render a template with the calculated distance
                        return render(request, self.template_name, context)
                    else:
                        form.add_error(None, "Distance calculation failed.")
                except Exception as e:
                    # Print the exception for debugging
                    print("Error during distance calculation:", e)
                    form.add_error(None, "Distance calculation failed.")
                    
        save_form_one = form.save()

        # Re-render the page with the form (and possibly errors)
        context = {
            'form_one': save_form_one,
            'form_two': LocationForm(),
            'form_trip':TripForm(),
            'distance_mile':distance_miles,
            'distances': Distances.objects.all(),  
            'locations': Locations.objects.all(),
            'trip': Trip.objects.all()
        }


        return render(request, self.template_name, context)
    
    def post_form_two(self,request):
        form_address = LocationForm(request.POST)
        if form_address.is_valid():
            form = form_address.save()
            context = {
            'form_one': DistanceForm(),  # Initialize a new form for distance calculation
            'form_two': LocationForm(),
            'form_trip':TripForm(),
            'distances': Distances.objects.all(),
            'locations': Locations.objects.all(),

            }
        return render(request, 'distance.html', context)
    
    def form_valid(self, form):
        form.instance.vehicle = Vehicle.objects.get(pk=self.kwargs.get('vehicle_id'))
        
        form.save()
        return super(CreateTrip, self).form_valid(form)
