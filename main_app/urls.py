from django.urls import path
from . import views



urlpatterns=[
    path('', views.home, name='home'),
    # path('user/', views.user, name='user_profile'),


    # CBV Paths

    # USER CBV
    # path('user/create/', views.CreateUser.as_view(), name='user_create'),#HANDLED BY AUTH?
    # path('user/<int:pk>/update/', views.UpdateUser.as_view(), name='user_update'),
    # path('user/<int:pk>/delete', views.DeleteUser.as_view(), name='user_delete'),


    # VEHICLE CBV
    path('accounts/vehicle/', views.VehicleList.as_view(), name='vehicle_list'),
    path('accounts/vehicle/create/', views.CreateVehicle.as_view(), name='vehicle_create'),
    path('accounts/vehicle/<int:vehicle_id>/update', views.UpdateVehicle.as_view(), name='vehicle_update'),
    path('accounts/vehicle/<int:vehicle_id>/delete', views.DeleteVehicle.as_view(), name='vehicle_delete'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),


    # TRIP CBV
    path('accounts/vehicle/<int:vehicle_id>/trip/', views.TripList.as_view(), name = 'trip_list'),
    path('accounts/vehicle/<int:vehicle_id>/trip/create/', views.CreateTrip.as_view(), name = 'trip_create'),
    path('accounts/vehicle/<int:vehicle_id>/trip/<int:pk>/update', views.UpdateTrip.as_view(), name = 'trip_update'),
    path('accounts/vehicle/<int:vehicle_id>/trip/<int:pk>/delete', views.delete_trip, name = 'trip_delete'),
    
    path('accounts/vehicle/<int:vehicle_id>/trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),

    # for API
    # path('weather/<str:city>/', views.weather),

    path('accounts/signup/', views.signup, name='signup')
]