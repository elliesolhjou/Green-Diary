from django.shortcuts import render
from .models import Trip, User

# Create your views here.
def home(request):
    return render(request, 'home.html')

def profile(request):
    user = User.objects.all()
    return render(request, 'profile/index.html', {'user':user})

def trip_index(request):
    trips = Trip.objects.all()
    return render(request, 'trip/index.html', {'trips':trips})

def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip.id)
    return render(request, 'trip/detail.html', {'trip':trip})