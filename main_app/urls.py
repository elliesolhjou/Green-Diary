from django.urls import path
from . import views



urlpatterns=[
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('trips/', views.trip_index, name='trip_index'),
    path('trips/<int:trip_id/', views.trip_detail, name='trip_detail'),
]