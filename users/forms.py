from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class UserForm(UserCreationForm):
    # this form is to create an user istance for the user 
    #widget to translate BE to html attrs and elements
    first_name = forms.CharField(max_length=30, required=True, widget = forms.TextInput(attrs = {'placeholder':'*Your Firstname'}))
    last_name = forms.CharField(max_length=30, required = True, widget=forms.TextInput(attrs = {'placeholder':'*Your Lastname'}))
    username = forms.EmailField(max_length=255, required=True, widget=forms.TextInput(attrs = {'placeholder':'*First Name Here'}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password..','class':'password'}))

    #reCaptcha
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2' )

class AuthForm(AuthenticationForm):
    # form for user login and auth
    username=forms.EmailField(max_length=254, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))

    class Meta:
        model=User
        fields=('username', 'password')



class UserProfileForm(forms.ModelForm):
    # generic django form class to cusotmize for user profile creation
    address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    town = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    county = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    post_code = forms.CharField(max_length=8, required=True, widget = forms.HiddenInput())
    country = forms.CharField(max_length=40, required=True, widget = forms.HiddenInput())
    longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
    latitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())


    class Meta:
        model = UserProfile
        fields = ('address', 'town', 'county', 'post_code',
        'country', 'longitude', 'latitude')
