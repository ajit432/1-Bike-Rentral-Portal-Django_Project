from django import forms
from django.contrib.auth.models import User
from customer.models import *
from renter.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        help_texts = {'username': ''}

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['username']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pno', 'profile_pic']
        widgets = {
            'pno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': 'image/*'
            }),
        }

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
        exclude = ['username', 'bike_name', 'booking_id', 'status', 'total_price', 'cancellation_reason', 'cancelled_at']
        widgets = {
            'pickup_date': DateInput(attrs={'id': 'id_pickup_date'}),
            'pickup_time': TimeInput(attrs={'id': 'id_pickup_time'}),
            'drop_date': DateInput(attrs={'id': 'id_drop_date'}),
            'drop_time': TimeInput(attrs={'id': 'id_drop_time'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        pickup_time = cleaned_data.get('pickup_time')
        drop_date = cleaned_data.get('drop_date')
        drop_time = cleaned_data.get('drop_time')
        
        if pickup_date and pickup_time and drop_date and drop_time:
            from datetime import datetime, date
            
            # Check if pickup date is not in the past
            if pickup_date < date.today():
                raise forms.ValidationError("Pickup date cannot be in the past.")
            
            # Check if drop date is not before pickup date
            if drop_date < pickup_date:
                raise forms.ValidationError("Drop date cannot be before pickup date.")
            
            # If same date, check if drop time is after pickup time
            if pickup_date == drop_date and drop_time <= pickup_time:
                raise forms.ValidationError("Drop time must be after pickup time on the same date.")
        
        return cleaned_data

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