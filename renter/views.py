from django.shortcuts import render
from customer.forms import *
from renter.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
from renter.forms import *

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
            return HttpResponseRedirect(reverse('newpw'))
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
    
    # Calculate total price for each booking
    for booking in allbookings:
        duration = (booking.drop_date - booking.pickup_date).days
        if duration > 0:
            booking.total_price = booking.bike_name.price_per_day * duration
        else:
            booking.total_price = booking.bike_name.price_per_day
        booking.duration_days = duration
    
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
    EBFO = BikeForm()
    d = {'EBFO': EBFO}
    if request.method == 'POST' and request.FILES:
        BFDO = BikeForm(request.POST, request.FILES)
        if BFDO.is_valid():
            BFDO.save()
            return HttpResponseRedirect(reverse('renter_home'))
    return render(request, 'renter/add_bikes.html', d)

def renter_display(request, brand):
    bikes = Bike.objects.filter(company=brand)
    d = {'bikes': bikes, 'brand': brand}
    return render(request, 'renter/renter_home.html', d)