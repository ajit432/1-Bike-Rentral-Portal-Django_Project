from django.urls import path
from renter.views import *

urlpatterns = [
    path('', renter_home, name='renter_home'),
    path('renter_register/', renter_register, name='renter_register'),
    path('renter_login/', renter_login, name='renter_login'),
    path('renter_logout/', renter_logout, name='renter_logout'),
    path('renter_display_profile/',  renter_display_profile, name='renter_display_profile'),
    path('renter_edit_profile/', renter_edit_profile, name='renter_edit_profile'),
    path('renter_forgetpw/', renter_forgetpw, name='renter_forgetpw'),
    path('renter_otp/', renter_otp, name='renter_otp'),
    path('renter_newpw/', newpw, name='renter_newpw'),
    path('renter_changepw/', renter_changepw, name='renter_changepw'),
    path('renter_display/<brand>', renter_display, name='renter_display'),
    path('allbooking/', allbooking, name ='allbooking'),
    path('approve/<int:pk>', approve, name='approve'),
    path('reject/<int:pk>', reject, name='reject'),
    path('add_bikes/', add_bikes, name='add_bikes'),
    path('my_bike_list/', my_bike_list, name='my_bike_list'),
    path('edit_bike/<int:bike_id>/', edit_bike, name='edit_bike'),
    path('delete_bike/<int:bike_id>/', delete_bike, name='delete_bike'),
    path('bike_details/<int:bike_id>/', bike_details, name='bike_details'),
]
