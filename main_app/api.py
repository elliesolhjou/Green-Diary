import requests


def get_makes():
    api_url = 'https://www.carboninterface.com/api/v1/vehicle_makes'
    headers = {
        'Authorization': 'Bearer sjXOxFgqEqHpfHKwvIclAg'
    }

    response = requests.get(api_url, headers = headers)
    if response.status_code == 200:
        print(response.json())
        makes_data = response.json()
        # makes_list = makes_data
        # return makes_list
        # print(makes_data['data']['attributes']['name'])

    else:
        print(response.status_code)
        response.raise_for_status()
        print(f"Error: {response.status_code}, {response.text}")