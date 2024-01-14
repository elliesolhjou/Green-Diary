import json
import os
from django.shortcuts import render
from django.conf import settings 

def home(request):
    vehicles_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/vehicles.json')
    trips_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/trips.json')

    with open(trips_path, 'r') as json_data:
        trip_data = json.load(json_data)

    with open(vehicles_path, 'r') as json_data:
        vehicle_data = json.load(json_data)

    return render(request, 'home.html', {'vehicles': vehicle_data, 'trips': trip_data})