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

class AccountView(TemplateView):
    template_name = "users/account.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Call the superclass method
        # dispatch is CRUD HANDLER -> The dispatch method examines the HTTP method of the request (in CBV)
        return super().dispatch(*args, **kwargs)