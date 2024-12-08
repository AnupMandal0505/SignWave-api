from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from app.models.location import SavedAddress
from app.serializers.LocationSerializer import SavedAddressSerializer
from django.contrib.auth.models import User




# from .models import SavedAddress
# from app.serializers.LocationSerializer import SavedAddressSerializer

permission_classes = [IsAuthenticated]  # Correct placement of permission
class SaveAddressAPI(APIView):
    def post(self, request):

        try:
            user_ref = request.user
            address = request.data.get('address')
            district = request.data.get('district')            
            pincode = request.data.get('pincode')
            state = request.data.get('state')
            country = request.data.get('country')            
            lattitude = request.data.get('lattitude')
            longitude = request.data.get('longitude')            
            locality = request.data.get('locality')
            
            # Ensure all required fields are provided
            if not all([state, district,country,pincode]):
                return Response(
                    {"message": "All fields are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            Address = SavedAddress.objects.create(user_ref=user_ref,address=address,district=district,pincode=pincode,state=state,country=country,lattitude=lattitude,longitude=longitude,locality=locality)
            return Response(
                        {"message": 'Address Saved Successful!'}, 
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






    # views.py

    def get(self, request):
        saved_addresses = SavedAddress.objects.filter(user_ref=request.user)
        
        serializer = SavedAddressSerializer(saved_addresses, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

          


    def put(self, request):
        """
        Update an existing call.
        """
        try:
            save_add = SavedAddress.objects.get(user_ref=request.user)  # Ensure the user is the sender
        except SavedAddress.DoesNotExist:
            return Response({"error": "Call not found or unauthorized access."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SavedAddressSerializer(save_add, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)