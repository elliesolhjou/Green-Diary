import json
import os
from datetime import datetime
from django.shortcuts import render
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