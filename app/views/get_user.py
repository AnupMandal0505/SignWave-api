from django.shortcuts import render,redirect,HttpResponse
import random
# from app.models import Patient,Appointment,Department
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ListSerializer, ValidationError

from app.serializers.userSerializer import UserSerializer,UpdateProfileSerializer

import json
from urllib.parse import unquote


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUser(request):
    user= request.user
    serializer = UserSerializer(user,many= False)
    print(serializer.data)
    return Response({"user":serializer.data})




@permission_classes([IsAuthenticated]) 
class UpdateProfileAPI(APIView):
    def put(self,request):
        serializer = UpdateProfileSerializer(instance=request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        else:
            # Log errors and return a helpful response
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)