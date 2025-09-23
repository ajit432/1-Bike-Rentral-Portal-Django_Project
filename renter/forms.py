from django import forms
from django.contrib.auth.models import User
from customer.models import *
from renter.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        help_texts = {'username': ''}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['username']

class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = '__all__'