from django.urls import path
from . import views


app_name ='users'

urlpatterns=[
    path("prfofileview", views.ProfileView.as_view(), name='profile-view'),
    path("profileupdate", views.ProfileUpdate.as_view(), name='profile-update'),
    path('sign-up', views.SignUpView.as_view(), name="sign-up"),
	path('sign-in', views.SignInView.as_view(), name="sign-in"),
	path('sign-out', views.sign_out, name="sign-out"),
	]

]