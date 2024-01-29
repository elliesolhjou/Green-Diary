from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from .forms import *
from greendiary.utility import *


# define global variable to be accessible 
result = "Error"
message= "There was an error, please try again"

# In Django's class-based views (CBVs), the dispatch method is quite central. 
# It is responsible for taking an HTTP request and dispatching it to the appropriate handler 
# method within the class based on the HTTP method (e.g., GET, POST, PUT, DELETE). 

# to view profile
class profileView(TemplateView):
    template_name = "users/profile.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Call the superclass method
        # dispatch is CRUD HANDLER -> The dispatch method examines the HTTP method of the request (in CBV)
        #  in CBV, if you are overwriting methods, should do super().overwriteMethod()
        return super().dispatch(*args, **kwargs)
    

# to update profile
class UpdateUser(UpdateView):
# def  UpdateUser(request):
    model = UserProfile
    fields = '__all__'
    # if request.method =='POST':
            
    #     form = UserProfileForm(request.POST)
    #     if form.is_valid():
    #         user_profile = form.save()
    #         user_profile_has_profile = True
    #         result='success' 
    #         message='Your profile has been updated successfully!'
    #     else:
    #         message= " Invalid. Please try again!"
    #         print("user profile update unsuccessful", form.errors)
                


