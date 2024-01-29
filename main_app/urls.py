from django.urls import path
from . import views


app_name ='main_app'

urlpatterns=[
    path('', views.home, name='home'),
    path('route', views.route, name='route'),
    path('map', views.map, name='map'),

    # CBV Paths

    # User Signup
    path('accounts/signup/', views.signup, name='signup'),

    # About Page
    path('about/', views.about, name='about'),

    # Vehicle
    path('accounts/vehicle/', views.VehicleList.as_view(), name='vehicle_list'),
    path('accounts/vehicle/create/', views.CreateVehicle.as_view(), name='vehicle_create'),
    path('accounts/vehicle/<int:pk>/update', views.UpdateVehicle.as_view(), name='vehicle_update'),
    path('accounts/vehicle/<int:vehicle_id>/delete', views.delete_vehicle, name='vehicle_delete'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),

    # Trip
    path('accounts/vehicle/<int:vehicle_id>/trip/', views.TripList.as_view(), name = 'trip_list'),
    path('accounts/vehicle/<int:vehicle_id>/trip/create/', views.CreateTrip.as_view(), name = 'trip_create'),
    path('accounts/vehicle/<int:vehicle_id>/trip/<int:pk>/update', views.UpdateTrip.as_view(), name = 'trip_update'),
    path('accounts/vehicle/<int:vehicle_id>/trip/<int:pk>/delete', views.delete_trip, name = 'trip_delete'),
    path('accounts/vehicle/<int:vehicle_id>/trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),

    #  Google Maps:
    path("route", views.route, name='route')
    path("map", views.map, name='map')

]