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
from app.views.otp import contact_us_send_company

class ContactAPI(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            message = request.data.get('message')

        
            if not (name and email and phone and message):
                return Response({'error': 'Required Field'}, status=status.HTTP_400_BAD_REQUEST)


            try:
                contact_us_send_company(request,email,name,phone,message)
                return Response({'Happy': 'Send Successful !'}, status=status.HTTP_200_OK)
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