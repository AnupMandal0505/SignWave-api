from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers.userSerializer import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User  # Use Django's default User model
from django.core.exceptions import ObjectDoesNotExist

class SignupAPI(APIView):

    def post(self, request):
        try:
            # Extract data from the request
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Ensure all required fields are provided
            if not all([username, email, password]):
                return Response(
                    {"message": "All fields are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(1)
            # Check if user already exists
            try:
                user = User.objects.get(username=username)
                return Response({"message": 'Email is already registered!'}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                # Create new user
                hashed_password = make_password(password)
                user = User.objects.create(username=username, email=email, password=hashed_password)

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
