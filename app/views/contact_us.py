from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

from django.shortcuts import redirect
# from app.models import ContactMessage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



def mail(name,email,phone):
    try:
        from_email = settings.EMAIL_HOST_USER
        
        # Correct template_path and render the HTML template with the provided data
        template_path = 'mail_templates/company.html'
        context = {
            'name': name,
            'contact': phone,
            'message':"message",
            'email':email,
        }
        
        subject="Contact For Bussiness"
        # Render the HTML template to a string
        message = render_to_string(template_path, context)
        
        to = "anupmandal828109@gmail.com"
        
        # Create an email message object and attach the HTML message
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(message, 'text/html')
        try:
            msg.send()
            clientmail(name,email)
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'Error sending email:',
                'message': 'Problem sending email check password',
                'data': {}
            }
            return Response(error_response, status=400)
        
    except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'Error sending email:',
                'message': 'Problem sending email check password',
                'data': {}
            }
            return Response(error_response, status=400)



def clientmail(name,email):
    try:
        from_email = settings.EMAIL_HOST_USER
        subject = "ABCD pvt.LTD"
        # Correct template_path and render the HTML template with the provided data
        template_path = 'mail_templates/client.html'
        context = {
            'name': name,
        }
        
        # Render the HTML template to a string
        message = render_to_string(template_path, context)
        
        to = email
        
        # Create an email message object and attach the HTML message
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(message, 'text/html')


        try:
            msg.send()
            return Response({'error': 'message send successful'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'Error sending email:',
                'message': 'Problem sending email check password',
                'data': {}
            }
            return Response(error_response, status=400)
    
    except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'Error sending email:',
                'message': 'Problem sending email check password',
                'data': {}
            }
            return Response(error_response, status=400)


class ContactAPI(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            
        
            if not (name and email and phone):
                return Response({'error': 'Required Field'}, status=status.HTTP_400_BAD_REQUEST)


            try:
                mail(name, email, phone)
                return Response({'HAppy': 'Send Successful !'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'There was a problem sending your message. Please try again later.'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Not get data',
                'data': {}
            }
            return Response(error_response, status=400)