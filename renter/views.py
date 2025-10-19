from django.shortcuts import render
from customer.forms import *
from renter.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
from renter.forms import *
from datetime import datetime
from decimal import Decimal

# Create your views here.

def renter_home(request):
    un = request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        brands = Brand.objects.all()
        bikes = Bike.objects.all()
        d = {'UO': UO, 'brands': brands, 'bikes': bikes}
        return render(request, 'renter/renter_home.html', d)
    brands = Brand.objects.all()
    bikes = Bike.objects.all()
    d = {'brands': brands, 'bikes': bikes} 
    return render(request, 'renter/renter_home.html', d)

def renter_register(request):
    EUFO = UserForm()
    ECFO = ProfileForm()
    d = {'EUFO': EUFO, 'ECFO': ECFO}
    if request.method == 'POST':
        print("CSRF token received:", request.POST.get('csrfmiddlewaretoken'))
        print("POST data:", request.POST)
        UFDO = UserForm(request.POST)
        CFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid() and CFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MCFDO = CFDO.save(commit=False)
            MCFDO.username = MUFDO
            MUFDO.is_staff = True
            MUFDO.save()
            MCFDO.save()
            return HttpResponseRedirect(reverse('renter_home'))
        else:
            # Debug: Print form errors
            print("User form errors:", UFDO.errors)
            print("Profile form errors:", CFDO.errors)
            return HttpResponse(f'Invalid Data. User errors: {UFDO.errors}, Profile errors: {CFDO.errors}')
    return render(request, 'renter/renter_register.html', d)


def renter_login(request):
    if request.method == 'POST':
        print("CSRF token received:", request.POST.get('csrfmiddlewaretoken'))
        print("POST data:", request.POST)
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        
        if not un or not pw:
            return HttpResponse('Please provide both username and password')
            
        AUO = authenticate(username=un, password=pw)
        
        if AUO is None:
            return HttpResponse('Invalid username or password')
        elif not AUO.is_staff:
            return HttpResponse('Access denied. Please use customer login.')
        elif AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('renter_home'))
        else:
            return HttpResponse('Account is not active. Please contact support.')

    return render(request, 'renter/renter_login.html')


def renter_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('renter_home'))

def renter_display_profile(request):
   un = request.session.get('username')
   if not un:
       return HttpResponse('Please login first')
   try:
       UO = User.objects.get(username=un)
       PO = Profile.objects.get(username=UO)
       d = {'UO': UO, 'PO': PO}
       return render(request, 'renter/renter_display_profile.html', d)
   except (User.DoesNotExist, Profile.DoesNotExist):
       return HttpResponse('Profile not found')

def renter_forgetpw(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        try:
            UO = User.objects.get(username=un)
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['username'] = un
            print(otp)
            return HttpResponseRedirect(reverse('renter_otp'))
        except User.DoesNotExist:
            return HttpResponse('User not found')
    return render(request, 'renter/renter_forgetpw.html')

def renter_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(otp) == gotp:
            return HttpResponseRedirect(reverse('renter_newpw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'renter/renter_otp.html')

def newpw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            if UO:
                UO.set_password(pw)
                UO.save()
                return HttpResponseRedirect(reverse('renter_login'))
            return HttpResponse('Session Expired')
        return HttpResponse('Password Does Not Match')
    return render(request, 'renter/newpw.html')

def renter_changepw(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    if UO:
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['username'] = un
        print(otp)
        return HttpResponseRedirect(reverse('renter_otp'))

def allbooking(request):
    allbookings = Booking.objects.all()
    
    # Calculate total price for each booking based on hourly rate
    for booking in allbookings:
        pickup_dt = datetime.combine(booking.pickup_date, booking.pickup_time)
        drop_dt = datetime.combine(booking.drop_date, booking.drop_time)
        # Use Decimal for precise monetary calculations and to avoid Decimal * float
        seconds = Decimal((drop_dt - pickup_dt).total_seconds())
        duration_hours = seconds / Decimal(3600)
        if duration_hours < Decimal('1'):
            duration_hours = Decimal('1')

        # Calculate and round to 2 decimal places for currency
        booking.total_price = (booking.bike_name.price_per_hour * duration_hours).quantize(Decimal('0.01'))
        booking.duration_hours = float(duration_hours)
    
    d = {'allbookings':allbookings}
    return render(request, 'renter/allbooking.html', d)

def approve(request, pk):
    if request.method == 'POST':
        BO = Booking.objects.get(pk=pk)
        BO.status = 'Approve'
        BO.save()
    return HttpResponseRedirect(reverse('allbooking'))

def reject(request, pk):
    if request.method == 'POST':
        BO = Booking.objects.get(pk=pk)
        BO.status = 'Reject'
        BO.save()
    return HttpResponseRedirect(reverse('allbooking'))
    

def add_bikes(request):
    un = request.session.get('username')
    if not un:
        return HttpResponse('Please login first')
    
    EBFO = BikeForm()
    d = {'EBFO': EBFO}
    if request.method == 'POST' and request.FILES:
        BFDO = BikeForm(request.POST, request.FILES)
        if BFDO.is_valid():
            bike = BFDO.save(commit=False)
            bike.renter = User.objects.get(username=un)
            bike.save()
            return HttpResponseRedirect(reverse('renter_home'))
    return render(request, 'renter/add_bikes.html', d)

def renter_display(request, brand):
    bikes = Bike.objects.filter(company=brand)
    d = {'bikes': bikes, 'brand': brand}
    return render(request, 'renter/renter_home.html', d)

def my_bike_list(request):
    un = request.session.get('username')
    if not un:
        return HttpResponse('Please login first')
    
    UO = User.objects.get(username=un)
    my_bikes = Bike.objects.filter(renter=UO)
    d = {'my_bikes': my_bikes, 'UO': UO}
    return render(request, 'renter/my_bike_list.html', d)

def edit_bike(request, bike_id):
    un = request.session.get('username')
    if not un:
        return HttpResponse('Please login first')
    
    try:
        bike = Bike.objects.get(id=bike_id, renter__username=un)
    except Bike.DoesNotExist:
        return HttpResponse('Bike not found or you do not have permission to edit this bike')
    
    if request.method == 'POST':
        # Update bike information
        bike.bike_name = request.POST.get('bike_name', bike.bike_name)
        bike.desc = request.POST.get('desc', bike.desc)
        bike.price_per_hour = request.POST.get('price_per_hour', bike.price_per_hour)
        
        # Handle brand update
        brand_name = request.POST.get('company')
        if brand_name:
            try:
                brand = Brand.objects.get(company=brand_name)
                bike.company = brand
            except Brand.DoesNotExist:
                # Create new brand if it doesn't exist
                brand = Brand.objects.create(company=brand_name)
                bike.company = brand
        
        # Handle photo update
        if 'photo' in request.FILES:
            bike.photo = request.FILES['photo']
        
        bike.save()
        return HttpResponseRedirect(reverse('my_bike_list'))
    
    # Get all brands for the dropdown
    brands = Brand.objects.all()
    d = {'bike': bike, 'brands': brands}
    return render(request, 'renter/edit_bike.html', d)

def delete_bike(request, bike_id):
    un = request.session.get('username')
    if not un:
        return HttpResponse('Please login first')
    
    try:
        bike = Bike.objects.get(id=bike_id, renter__username=un)
    except Bike.DoesNotExist:
        return HttpResponse('Bike not found or you do not have permission to delete this bike')
    
    if request.method == 'POST':
        bike.delete()
        return HttpResponseRedirect(reverse('my_bike_list'))
    
    d = {'bike': bike}
    return render(request, 'renter/delete_bike.html', d)

def bike_details(request, bike_id):
    try:
        bike = Bike.objects.get(id=bike_id)
        d = {'bike': bike}
        return render(request, 'renter/bike_details.html', d)
    except Bike.DoesNotExist:
        return HttpResponse('Bike not found')

def renter_edit_profile(request):
    un = request.session.get('username')
    if not un:
        return HttpResponse('Please login first')
    
    try:
        UO = User.objects.get(username=un)
        PO = Profile.objects.get(username=UO)
        
        if request.method == 'POST':
            # Update User model
            UO.first_name = request.POST.get('first_name', UO.first_name)
            UO.last_name = request.POST.get('last_name', UO.last_name)
            UO.email = request.POST.get('email', UO.email)
            UO.save()
            
            # Update Profile model
            PO.pno = request.POST.get('pno', PO.pno)
            if 'profile_pic' in request.FILES:
                PO.profile_pic = request.FILES['profile_pic']
            PO.save()
            
            return HttpResponseRedirect(reverse('renter_display_profile'))
        
        # Pre-populate forms with current data
        EUFO = UserForm(instance=UO)
        ECFO = ProfileForm(instance=PO)
        d = {'EUFO': EUFO, 'ECFO': ECFO, 'UO': UO, 'PO': PO}
        return render(request, 'renter/renter_edit_profile.html', d)
        
    except (User.DoesNotExist, Profile.DoesNotExist):
        return HttpResponse('Profile not found')