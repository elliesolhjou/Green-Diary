import requests


def get_makes():
    api_url = 'https://www.carboninterface.com/api/v1/vehicle_makes'
    headers = {
        'Authorization': 'Bearer sjXOxFgqEqHpfHKwvIclAg'
    }

    response = requests.get(api_url, headers = headers)
    if response.status_code == 200:
        makes_data = response.json()
        makes_list = [(make['id'], make['attributes']['name']) for make in makes_data['data']]
        return makes_list

    else:
        print(response.status_code)
        response.raise_for_status()
        print(f"Error: {response.status_code}, {response.text}")



def get_models_for_make(make_id):
    api_url = f'https://www.carboninterface.com/api/v1/vehicle_makes/{make_id}/models'
    headers = {
        'Authorization': 'Bearer sjXOxFgqEqHpfHKwvIclAg'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        models_data = response.json()
        # Assuming each model has an 'attributes' with a 'name' key
        models_list = [(model['id'], model['attributes']['name']) for model in models_data['data']]
        return models_list
    else:
        response.raise_for_status()