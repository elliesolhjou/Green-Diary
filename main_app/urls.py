from django.urls import path
from . import views



urlpatterns=[
    path('', views.home, name='home'),
    path('user/', views.user, name='user_profile'),


    # CBV Paths

    # USER CBV
    path('user/create/', views.CreateUser.as_view(), name='user_create'),#HANDLED BY AUTH?
    path('user/<int:pk>/update/', views.UpdateUser.as_view(), name='user_update'),
    path('user/<int:pk>/delete', views.DeleteUser.as_view(), name='user_delete'),


    # VEHICLE CBV
    path('vehicle/', views.VehicleList.as_view(), name='vehicle_list'),
    path('vehicle/create/', views.CreateVehicle.as_view(), name='vehicle_create'),
    path('vehicle/<int:vehicle_id>/update', views.UpdateVehicle.as_view(), name='vehicle_update'),
    path('vehicle/<int:vehicle_id>/delete', views.DeleteVehicle.as_view(), name='vehicle_delete'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),


    # TRIP CBV
    path('trip/', views.TripList.as_view(), name = 'trip_list'),
    path('trip/create/', views.CreateTrip.as_view(), name = 'trip_create'),
    path('trip/<int:pk>/update', views.UpdateTrip.as_view(), name = 'trip_update'),
    path('trip/<int:pk>/delete', views.delete_trip, name = 'trip_delete'),
    
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),


]