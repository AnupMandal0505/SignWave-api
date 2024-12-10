from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from datetime import datetime


def send_otp_email(request, template_path, subject, context):
    try:
        from_email = settings.EMAIL_HOST_USER
        message = render_to_string(template_path, context)
        to = context['email']
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(message, 'text/html')
        msg.send()
        return JsonResponse({'success': 'OTP sent successfully to your email.'}, status=200)
    except Exception as e:
        print("Error sending email:", e)
        return JsonResponse({'error': 'Problem sending email. Please try again later.'}, status=500)

@api_view(['POST'])
def user_verify(request):
    email = request.data.get('email')
    name = request.data.get('name')
    otp = request.data.get('otp')
    if not email or not name:
        return JsonResponse({'error': 'Email and name are required.'}, status=400)
    context = {'name': name, 'otp': otp, 'email': email}
    return send_otp_email(request, 'mail_templates/user_otp_verify.html', 'Complete Your Signup – Enter Your OTP', context)

@api_view(['POST'])
def account_create_successful(request):
    email = request.data.get('email')
    name = request.data.get('name')
    username = request.data.get('username')
    password = request.data.get('password')
    if not email:
        return JsonResponse({'error': 'Email is required.'}, status=400)
    context = {'email': email,'name': name,'username': username,'password':password}
    return send_otp_email(request, 'mail_templates/account_create_successful.html', 'Account Creation Successful', context)



def contact_us_send_company(request,user_email,name,phone,message):
    if not user_email or not name or not phone:
        return JsonResponse({'error': 'Email and name are required.'}, status=400)
    context = {'name': name, 'message': message, 'user_email': user_email,'email': "anup.mandal.ds25@heritageit.edu.in"}
    contact_us_client(request,user_email,name)
    return send_otp_email(request, 'mail_templates/contact_us_send_company.html', 'Request for Contact', context)


def contact_us_client(request,email,name):

    if not email or not name:
        return JsonResponse({'error': 'Email and name are required.'}, status=400)
    context = {'name': name, 'email': email}
    return send_otp_email(request, 'mail_templates/contact_us_client.html', 'Thank You for Reaching Out to Us!', context)




def payment(request, email, name, transaction_amount, payment_id,bit_coin):
    if not email:
        return JsonResponse({'error': 'Email is required.'}, status=400)

    # Context to pass to the email template
    context = {
        'transaction_amount': transaction_amount,
        'payment_id': payment_id,
        'email': email,
        'name': name,
        'bit_coin':bit_coin,
    }
    
    # Send email using the email template
    return send_otp_email(request, 'mail_templates/payment.html', 'Payment Received Successfully', context)
    
    # Response back after sending the email
    # return JsonResponse({'message': 'Payment confirmation email sent successfully.'})




def create_video_callte_mail(request,receiver_email,receiver_name,meetingtime,sender_email,sender_name):
    date_part, time_part = meetingtime.split('T')

    # Convert the date part and time part into separate datetime objects if needed
    date = datetime.strptime(date_part, '%Y-%m-%d').date()
    time = datetime.strptime(time_part, '%H:%M:%S').time()

    if not receiver_email or not receiver_name:
        return JsonResponse({'error': 'Email and name are required.'}, status=400)
    context = {'receiver_name': receiver_name, 'date': date,'time':time, 'email': receiver_email,'sender_name':sender_name,'sender_email':sender_email}
    return send_otp_email(request, 'mail_templates/video_call.html', f'{sender_name}: Your 3Video Call', context)




from django.contrib.auth.models import User

def video_call_update_mail(request,receiver,meetingtime,sender_email,sender_name):
    user=User.objects.get(username=receiver)
    receiver_email=user.email
    receiver_name=user.first_name

# Ensure meetingtime is a string, if it's not, convert it
    if isinstance(meetingtime, datetime):
        # If it's already a datetime object, convert it to string in ISO format
        meetingtime = meetingtime.isoformat()
    elif not isinstance(meetingtime, str):
        # If it's not a string, raise an error
        raise ValueError("Invalid meeting time format. Expected a string.")

    datetime_obj = datetime.fromisoformat(meetingtime)

    # Split the date and time
    date = datetime_obj.date()   # Extract the date part
    time = datetime_obj.time()

    if not receiver_email or not receiver_name:
        raise ValueError("Receiver email and name are required.")
    context = {'receiver_name': receiver_name, 'date': date,'time':time, 'email': receiver_email,'sender_name':sender_name,'sender_email':sender_email}
    return send_otp_email(request, 'mail_templates/update_video_call.html', 'Update: Video Call Rescheduled', context)
