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

class DateInput(forms.DateInput):
    input_type = 'date'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'placeholder': 'dd-mm-yyyy',
            'style': 'background: var(--bg-primary); border: 2px solid var(--border-color); border-radius: 12px; color: var(--text-primary); padding: 15px 20px; font-size: 1rem; transition: all 0.3s ease; backdrop-filter: blur(10px); min-height: 48px;',
            'autocomplete': 'off',
            'required': 'required'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class TimeInput(forms.TimeInput):
    input_type = 'time'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'placeholder': '--:-- --',
            'style': 'background: var(--bg-primary); border: 2px solid var(--border-color); border-radius: 12px; color: var(--text-primary); padding: 15px 20px; font-size: 1rem; transition: all 0.3s ease; backdrop-filter: blur(10px); min-height: 48px;',
            'autocomplete': 'off',
            'required': 'required'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['username', 'bike_name', 'booking_id', 'status']
        widgets = {
            'pickup_date': DateInput(attrs={'id': 'id_pickup_date'}),
            'pickup_time': TimeInput(attrs={'id': 'id_pickup_time'}),
            'drop_date': DateInput(attrs={'id': 'id_drop_date'}),
            'drop_time': TimeInput(attrs={'id': 'id_drop_time'})
        }

class CancelBookingForm(forms.Form):
    cancellation_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Please provide a reason for cancelling this booking...',
            'class': 'form-control'
        }),
        label='Cancellation Reason',
        help_text='Please explain why you want to cancel this booking.',
        max_length=500,
        required=True
    )