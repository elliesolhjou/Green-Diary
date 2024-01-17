from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class VehicleForm(forms.ModelForm):
    pass
#     class Meta:
#         model = Vehicle
#         fields= ['make', 'model', 'year', 'fuel']
# 
#         widgets ={
#             'make': forms.Select(attrs={'class': 'form-control'}),
#             'model': forms.TextInput(attrs={'class': 'form-control'}),
#             'year': forms.NumberInput(attrs={'class': 'form-control'}),
#             'fuel_type': forms.Select(attrs={'class': 'form-control'}),
#         }
# 
#         # custom validation
#         def clean_year(self):
#             year = self.cleaned_data.get('year')
#             if year and year > 2024:  # Just an example condition
#                 raise forms.ValidationError('Please enter a valid year.')
#             return year
#         
# 
#         # You can also add a __init__ method if you need to dynamically set choices for a field, like 'make'
#         def __init__(self, *args, **kwargs):
#             super(VehicleForm, self).__init__(*args, **kwargs)
#             # Dynamically set the choices for the 'make' field
#             self.fields['make'].choices = get_makes()