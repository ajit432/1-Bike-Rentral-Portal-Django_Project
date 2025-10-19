from django.shortcuts import render
from customer.forms import *
from renter.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import random
from renter.models import *
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

# Create your views here.

def home(request):
    un = request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        brands = Brand.objects.all()
        bikes = Bike.objects.all()
        d = {'UO': UO, 'brands': brands, 'bikes': bikes}
        return render(request, 'customer/home.html', d)
    brands = Brand.objects.all()
    bikes = Bike.objects.all()
    d = {'brands': brands, 'bikes': bikes}    
    return render(request, 'customer/home.html', d)


def register(request):
    EUFO = UserForm()
    ECFO = ProfileForm()
    d = {'EUFO': EUFO, 'ECFO': ECFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        CFDO = ProfileForm(request.POST,request.FILES)


        if UFDO.is_valid() and CFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MCFDO = CFDO.save(commit=False)
            MCFDO.username = MUFDO
            MUFDO.save()
            MCFDO.save()
            # ✅ Send confirmation email
            subject = 'Welcome to Bike Rental System!'
            message = f"""
                Hello {MUFDO.first_name or MUFDO.username},
                Thank you for registering with our Bike Rental System.
                You can now log in and start booking bikes easily.
                Happy riding! 🏍️
                - Bike Rental Team
                """
            recipient = MUFDO.email
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            except Exception as e:
                print("line-60 Email sending failed:", e)

            return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('Invalid Data')
    return render(request, 'customer/register.html', d)


def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        
        if not un or not pw:
            return HttpResponse('Please provide both username and password')
            
        AUO = authenticate(username=un, password=pw)
        
        if AUO is None:
            return HttpResponse('Invalid username or password')
        elif AUO.is_staff:
            return HttpResponse('Access denied. Please use renter login.')
        elif AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Account is not active. Please contact support.')

    return render(request, 'customer/user_login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def forgetpw(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        try:
            UO = User.objects.get(username=un)
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['username'] = un
            print(f"line-104 This is the otp for customoer forgot password {otp}")
            send_mail(
                'Your Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                settings.EMAIL_HOST_USER,
                [UO.email],
                fail_silently=False,
            )
            return HttpResponseRedirect(reverse('otp'))
        except User.DoesNotExist:
            return HttpResponse('User not found')
    return render(request, 'customer/forgetpw.html')


def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(otp) == gotp:
            return HttpResponseRedirect(reverse('newpw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'customer/otp.html')


def newpw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('username')
            try:
                UO = User.objects.get(username=un)
                UO.set_password(pw)
                UO.save()
                return HttpResponseRedirect(reverse('user_login'))
            except User.DoesNotExist:
                return HttpResponse('Session expired')         
        return HttpResponse("Password doesn't Match")      
    return render(request, 'customer/newpw.html') 


def changepw(request):
    un = request.session.get('username')
    if not un:
        return HttpResponse('Please login first')
    try:
        UO = User.objects.get(username=un)
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['username'] = un
        print(otp)
        return HttpResponseRedirect(reverse('otp'))
    except User.DoesNotExist:
        return HttpResponse('User not found')
    

def display_profile(request):
   un = request.session.get('username')
   if not un:
       return HttpResponse('Please login first')
   try:
       UO = User.objects.get(username=un)
       PO = Profile.objects.get(username=UO)
       d = {'UO': UO, 'PO': PO}
       return render(request, 'customer/display_profile.html', d)
   except (User.DoesNotExist, Profile.DoesNotExist):
       return HttpResponse('Profile not found')

def edit_profile(request):
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
            
            return HttpResponseRedirect(reverse('display_profile'))
        
        # Pre-populate forms with current data
        EUFO = UserForm(instance=UO)
        ECFO = ProfileForm(instance=PO)
        d = {'EUFO': EUFO, 'ECFO': ECFO, 'UO': UO, 'PO': PO}
        return render(request, 'customer/edit_profile.html', d)
        
    except (User.DoesNotExist, Profile.DoesNotExist):
        return HttpResponse('Profile not found')

def display(request, brand):
    bikes = Bike.objects.filter(company=brand)
    d = {'bikes': bikes, 'brand': brand}
    return render(request, 'customer/home.html', d)

def book(request, pk):
    un = request.session.get('username')
    if un:
        bike = Bike.objects.get(pk=pk)
        EBFO = BookingForm()
        d = {'bike': bike, 'EBFO': EBFO}
        if request.method == 'POST':
            BFDO = BookingForm(request.POST)
            UO = User.objects.get(username=un)
            BO = Bike.objects.get(pk=pk)
            bookings = Booking.objects.filter(bike_name=BO)
            for booking in bookings:
                if str(booking.pickup_date) == request.POST.get('pickup_date'):
                    return render(request, 'customer/not_avail.html')
            MBFDO = BFDO.save(commit=False)
            MBFDO.username = UO
            MBFDO.bike_name=bike
            # Calculate total price based on hourly rate
            pickup_dt = datetime.combine(MBFDO.pickup_date, MBFDO.pickup_time)
            drop_dt = datetime.combine(MBFDO.drop_date, MBFDO.drop_time)
            duration_hours = (drop_dt - pickup_dt).total_seconds() / 3600
            if duration_hours < 1:
                duration_hours = 1

            # Use hourly rate directly
            MBFDO.total_price = Decimal(bike.price_per_hour) * Decimal(duration_hours)

            MBFDO.save()
            return render(request, 'customer/conf.html')
        return render(request, 'customer/book.html', d)
    return HttpResponseRedirect(reverse('user_login'))

def search(request):
    if request.method == 'POST':
        bike = request.POST.get('srch')
        BO = Bike.objects.get(bike_name=bike)
        d = {'BO': BO}
        return render(request, 'customer/display.html', d)   
    
def show(request, pk):
    BO = Bike.objects.get(pk=pk)
    d = {'BO': BO}
    return render(request, 'customer/display.html', d)   

def my_bookings(request):
    un =  request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        bookings = Booking.objects.filter(username=UO)
        
        # Calculate total price for each booking based on hourly rate
        for booking in bookings:
            pickup_dt = datetime.combine(booking.pickup_date, booking.pickup_time)
            drop_dt = datetime.combine(booking.drop_date, booking.drop_time)
            duration_hours = (drop_dt - pickup_dt).total_seconds() / 3600
            if duration_hours < 1:
                duration_hours = 1
            
            booking.total_price = booking.bike_name.price_per_hour * duration_hours
            booking.duration_hours = duration_hours
        
        d = {'bookings': bookings}
        return render(request, 'customer/my_bookings.html', d)

def cancel_booking(request, booking_id):
    if request.session.get('username'):
        try:
            booking = Booking.objects.get(booking_id=booking_id, username__username=request.session.get('username'))
            
            if booking.status != 'Pending':
                messages.error(request, 'Only pending bookings can be cancelled.')
                return HttpResponseRedirect(reverse('my_bookings'))
            
            if request.method == 'POST':
                form = CancelBookingForm(request.POST)
                if form.is_valid():
                    booking.cancellation_reason = form.cleaned_data['cancellation_reason']
                    booking.status = 'Cancelled'
                    booking.cancelled_at = timezone.now()
                    booking.save()
                    messages.success(request, 'Booking cancelled successfully.')
                    return HttpResponseRedirect(reverse('my_bookings'))
            else:
                form = CancelBookingForm()
            
            d = {'booking': booking, 'form': form}
            return render(request, 'customer/cancel_booking.html', d)
            
        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
            return HttpResponseRedirect(reverse('my_bookings'))
    
    return HttpResponseRedirect(reverse('user_login'))
    return HttpResponse('Invalid User')