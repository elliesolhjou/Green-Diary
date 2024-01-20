import requests
import json
 
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

