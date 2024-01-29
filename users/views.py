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
class ProfileView(TemplateView):
    template_name = "users/profile.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Call the superclass method
        # dispatch is CRUD HANDLER -> The dispatch method examines the HTTP method of the request (in CBV)
        #  in CBV, if you are overwriting methods, should do super().overwriteMethod()
        return super().dispatch(*args, **kwargs)
    

# to update profile
# class ProfileUpdate(UpdateView):
# def  UpdateUser(request):
    # model = UserProfile
    # fields = '__all__'
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
                

# delete user
def ProfileUpdate(request):
	'''
	function view to allow users to update their profile
	'''
	user = request.user
	up = user.userprofile

	form = UserProfileForm(instance = up) 

	if request.is_ajax():
		form = UserProfileForm(data = request.POST, instance = up)
		if form.is_valid():
			obj = form.save()
			obj.has_profile = True
			obj.save()
			result = "Success"
			message = "Your profile has been updated"
		else:
			message = FormErrors(form)
		data = {'result': result, 'message': message}
		return JsonResponse(data)

	else:

		context = {'form': form}
		context['google_api_key'] = settings.GOOGLE_API_KEY
		context['base_country'] = settings.BASE_COUNTRY

		return render(request, 'users/profile.html', context)



class SignUpView(AjaxFormMixin, FormView):
	'''
	Generic FormView with our mixin for user sign-up with reCAPTURE security
	'''

	template_name = "users/sign_up.html"
	form_class = UserForm
	success_url = "/"

	#reCAPTURE key required in context
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["recaptcha_site_key"] = settings.RECAPTCHA_PUBLIC_KEY
		return context

	#over write the mixin logic to get, check and save reCAPTURE score
	def form_valid(self, form):
		response = super(AjaxFormMixin, self).form_valid(form)	
		if self.request.is_ajax():
			token = form.cleaned_data.get('token')
			captcha = reCAPTCHAValidation(token)
			if captcha["success"]:
				obj = form.save()
				obj.email = obj.username
				obj.save()
				up = obj.userprofile
				up.captcha_score = float(captcha["score"])
				up.save()
				
				login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')

				#change result & message on success
				result = "Success"
				message = "Thank you for signing up"

				
			data = {'result': result, 'message': message}
			return JsonResponse(data)

		return response




class SignInView(AjaxFormMixin, FormView):
	'''
	Generic FormView with our mixin for user sign-in
	'''

	template_name = "users/sign_in.html"
	form_class = AuthForm
	success_url = "/"

	def form_valid(self, form):
		response = super(AjaxFormMixin, self).form_valid(form)	
		if self.request.is_ajax():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			#attempt to authenticate user
			user = authenticate(self.request, username=username, password=password)
			if user is not None:
				login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
				result = "Success"
				message = 'You are now logged in'
			else:
				message = FormErrors(form)
			data = {'result': result, 'message': message}
			return JsonResponse(data)
		return response




def sign_out(request):
	'''
	Basic view for user sign out
	'''
	logout(request)
	return redirect(reverse('users:sign-in'))