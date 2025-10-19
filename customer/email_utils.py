from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_notification(subject, message, recipient_email, html_message=None):
    """
    Utility function to send email notifications
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,
            html_message=html_message
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def send_registration_email(user):
    """Send welcome email after successful registration"""
    subject = 'Welcome to Bike Rental System!'
    message = f"""
Hello {user.first_name or user.username},

Thank you for registering with our Bike Rental System!
You can now log in and start booking bikes easily.

Happy riding! 🏍️

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, user.email)

def send_login_notification(user):
    """Send login notification email"""
    subject = 'Login Notification - Bike Rental System'
    message = f"""
Hello {user.first_name or user.username},

You have successfully logged into your Bike Rental account.

If this wasn't you, please contact our support team immediately.

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, user.email)

def send_logout_notification(user):
    """Send logout notification email"""
    subject = 'Logout Notification - Bike Rental System'
    message = f"""
Hello {user.first_name or user.username},

You have successfully logged out from your Bike Rental account.

Thank you for using our service!

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, user.email)

def send_otp_email(user, otp):
    """Send OTP for password reset"""
    subject = 'Your Password Reset OTP - Bike Rental System'
    message = f"""
Hello {user.first_name or user.username},

Your OTP for password reset is: {otp}

This OTP is valid for 10 minutes. Please do not share this OTP with anyone.

If you didn't request this, please ignore this email.

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, user.email)

def send_booking_confirmation_email(booking):
    """Send booking confirmation email to customer"""
    subject = 'Booking Confirmation - Bike Rental System'
    message = f"""
Hello {booking.username.first_name or booking.username.username},

Your bike booking has been confirmed!

Booking Details:
- Booking ID: {booking.booking_id}
- Bike: {booking.bike_name.bike_name}
- Pickup Date: {booking.pickup_date}
- Pickup Time: {booking.pickup_time}
- Drop Date: {booking.drop_date}
- Drop Time: {booking.drop_time}
- Total Price: ₹{booking.total_price}
- Status: {booking.status}

Please arrive on time for pickup.

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, booking.username.email)

def send_booking_notification_to_renter(booking):
    """Send new booking notification to bike renter"""
    subject = 'New Booking Request - Bike Rental System'
    message = f"""
Hello {booking.bike_name.renter.first_name or booking.bike_name.renter.username},

You have received a new booking request for your bike!

Booking Details:
- Booking ID: {booking.booking_id}
- Bike: {booking.bike_name.bike_name}
- Customer: {booking.username.first_name or booking.username.username}
- Customer Email: {booking.username.email}
- Pickup Date: {booking.pickup_date}
- Pickup Time: {booking.pickup_time}
- Drop Date: {booking.drop_date}
- Drop Time: {booking.drop_time}
- Total Price: ₹{booking.total_price}

Please log in to approve or reject this booking.

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, booking.bike_name.renter.email)

def send_booking_status_update_email(booking):
    """Send booking status update email to customer"""
    subject = f'Booking {booking.status} - Bike Rental System'
    
    if booking.status == 'Approve':
        message = f"""
Hello {booking.username.first_name or booking.username.username},

Great news! Your booking has been APPROVED!

Booking Details:
- Booking ID: {booking.booking_id}
- Bike: {booking.bike_name.bike_name}
- Pickup Date: {booking.pickup_date}
- Pickup Time: {booking.pickup_time}
- Drop Date: {booking.drop_date}
- Drop Time: {booking.drop_time}
- Total Price: ₹{booking.total_price}

Please arrive on time for pickup. Contact the renter if you have any questions.

Best regards,
Bike Rental Team
        """
    elif booking.status == 'Reject':
        message = f"""
Hello {booking.username.first_name or booking.username.username},

We regret to inform you that your booking has been REJECTED.

Booking Details:
- Booking ID: {booking.booking_id}
- Bike: {booking.bike_name.bike_name}
- Pickup Date: {booking.pickup_date}
- Pickup Time: {booking.pickup_time}

You can try booking other available bikes or contact support for assistance.

Best regards,
Bike Rental Team
        """
    elif booking.status == 'Cancelled':
        message = f"""
Hello {booking.username.first_name or booking.username.username},

Your booking has been CANCELLED as requested.

Booking Details:
- Booking ID: {booking.booking_id}
- Bike: {booking.bike_name.bike_name}
- Pickup Date: {booking.pickup_date}
- Pickup Time: {booking.pickup_time}
- Cancellation Reason: {booking.cancellation_reason}

If you have any questions, please contact our support team.

Best regards,
Bike Rental Team
        """
    else:
        message = f"""
Hello {booking.username.first_name or booking.username.username},

Your booking status has been updated to: {booking.status}

Booking Details:
- Booking ID: {booking.booking_id}
- Bike: {booking.bike_name.bike_name}
- Status: {booking.status}

Best regards,
Bike Rental Team
        """
    
    return send_email_notification(subject, message, booking.username.email)

def send_bike_added_notification(bike):
    """Send notification to renter when bike is successfully added"""
    subject = 'Bike Successfully Added - Bike Rental System'
    message = f"""
Hello {bike.renter.first_name or bike.renter.username},

Your bike has been successfully added to our platform!

Bike Details:
- Bike Name: {bike.bike_name}
- Brand: {bike.company.company}
- Price per Hour: ₹{bike.price_per_hour}
- Description: {bike.desc}

Your bike is now available for customers to book.

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, bike.renter.email)

def send_renter_registration_email(user):
    """Send welcome email to new renter"""
    subject = 'Welcome to Bike Rental System - Renter Account!'
    message = f"""
Hello {user.first_name or user.username},

Welcome to our Bike Rental System as a RENTER!

You can now:
- Add your bikes to the platform
- Manage booking requests
- Track your earnings

Start adding your bikes and earn money today!

Best regards,
Bike Rental Team
    """
    return send_email_notification(subject, message, user.email)