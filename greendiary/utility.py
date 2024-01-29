# utility functions here
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json
import datetime
from humanfriendly import format_timespan
from django.http import JsonResponse

# handling form errors passed to AJAX
def FormErrors(*args):
    message=""
    for f in args:
        if f.errors:
            message =f.errors.as_text()

        return message
    


def reCAPTCHAValidation(token):
    print(requests)

    # MAKING API CALL
    result = requests.post(
        'https:///www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token
        }
    )

    print('reCaptcha validation result:', result)
    return result.json()


def RedirectParams(**kwargs):
    # after user logs in -> append url in address bar/update address bar url
    url = kwargs.get('url')
    params=kwargs.get('params')
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location']+='?'+query_string

    return response

# to ajaxify this file ->(use utility to make BE&Fe communicate) 
class AjaxForUtility(object):
    def form_invalid(self, form):
        response = super(AjaxForUtility, self).form_invalid(form)
        if self.request.is_ajax():
            message = FormErrors(form)
            return JsonResponse({'result':'Error', 'message':message})
        
        return response



# HANDLING DIRS FROM GOOGLE MAPS
    
def Directions(*args, **kwargs):
    lat_a=kwargs.get('lat_a')
    long_a=kwargs.get('long_a')
    lat_b=kwargs.get('lat_b')
    long_b=kwargs.get('long_b')

# google maps expects origin not departure
    origin=f'{lat_a},{long_a}'
    destination=f'{lat_b},{long_b}'


    #MAKING API CALL
    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            "destination": destination,
            "key":settings.SECRET_KEY
        }
    )
    directions = result.json()

    if directions['status'] == "OK":
        routes = directions["routes"][0]["legs"]
        distance = 0
        duration = 0
        route_list = []

        for route in range(len(routes)):
            distance += int(routes[route["distance"]["value"]])
            duration += int(routes[route["duration"]["value"]])

# to structure and store information about each leg of the route obtained from the Google Maps Directions API -> route_step
#  leg is the segment of path/journey from origin/waypoint1 to destination or any other waypoint2
            route_step={
                'origin': routes[route]["start_address"],
                'destination': routes[route]["end_address"],
                'distance': routes[route]["distance"]["text"],
                'duration': routes[route]["duration"]["text"],
                'steps':[
                    [
                        s["distance"]["text"],
                        s["durations"]["text"],
                        s["html_instruction"]
                    ]
                    for s in routes[route]['steps']]
            }

            route_list.append(route_step)
    
    return {
        'origin': origin,
        "destination": destination,
        'distance': f"{round(distance*0.00062137, 2)} Km",
		"duration": format_timespan(duration),
		"route": route_list
    }
