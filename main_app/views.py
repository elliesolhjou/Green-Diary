import json
import os
from django.shortcuts import render
from django.conf import settings 

def home(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'main_app/static/data/vehicles.json')

    with open(json_file_path, 'r') as json_data:
        vehicle_data = json.load(json_data)

    return render(request, 'home.html', {'vehicles': vehicle_data})