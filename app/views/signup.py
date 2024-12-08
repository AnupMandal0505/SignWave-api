from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers.userSerializer import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User  # Use Django's default User model
from django.core.exceptions import ObjectDoesNotExist
from app.models.point import PointRecord

import random

def generate_unique_id():
    prefix = "sw"
    random_number = str(random.randint(1000, 9999))  # Random number for additional uniqueness
    id=prefix + random_number
    try:
        user = User.objects.get(username=id)
        generate_unique_id()
    except:
        return id



class SignupAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            
            # Ensure all required fields are provided
            if not all([email, password]):
                return Response(
                    {"message": "All fields are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(1)
            # Check if user already exists
            try:
                user = User.objects.get(email=email)
                return Response({"message": 'Email is already registered!'}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                # Create new user
                username = generate_unique_id()

                hashed_password = make_password(password)
                user = User.objects.create(username=username, email=email, password=hashed_password,first_name=first_name,last_name=last_name)
                PointRecord.objects.create(
                            user_ref=user, receiver="Sign Wave", status="success", details="Bonus",balance=0
                )
                # Optionally, use a serializer for validation (better practice)
                user_serializer = UserSerializer(user)
                return Response(
                    {"message": 'Registration Successful!', "data": user_serializer.data}, 
                    status=status.HTTP_201_CREATED
                )
        
        except Exception as e:
            return Response(
                {
                    'status': 400,
                    'error': 'something_went_wrong',
                    'message': str(e),  # Debugging information, remove in production
                    'data': {}
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
