from django.shortcuts import render,redirect,HttpResponse
import random
# from app.models import Patient,Appointment,Department
from django.contrib import messages
from app.models import User

   
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ListSerializer, ValidationError

from app.serializers.userSerializer import UserSerializer

import json
from urllib.parse import unquote


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUser(request):
    user= request.user
    serializer = UserSerializer(user,many= False)
    print(serializer.data)
    return Response({"user":serializer.data})

# def getUserByType(user_ref, filter):
#     DWC = {
#         "state_waste_collector_ref__user_ref": user_ref
#     }

#     WC = {
#         "district_waste_collector_ref__state_waste_collector_ref__user_ref": user_ref
#     }
#     USER = {
#         "user_type":"USER"
#     }
#     ResponseData = []

#     # UserDistrictCollectorSerializer
#     DWCdata = UserDistrictCollectorSerializer(DistrictWasteCollector.objects.filter(**DWC, **filter), many=True)
#     ResponseData += DWCdata.data

#     # UserWasteCollectorSerializer
#     WCdata = UserWasteCollectorSerializer(WasteCollector.objects.filter(**WC, **filter), many=True)
#     ResponseData += WCdata.data

#     # UserSerializer with ListSerializer
#     user_list = User.objects.filter(**USER, **filter)
#     print(user_list)
#     Userdata = UserSerializer(user_list, many=True)
#     ResponseData += list(Userdata.data)

#     return ResponseData

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def GetUserALL(request):
#     try:
#         # print("params",type(request.query_params.get("name")))
#         # Get the encoded filter from the query parameters
#         encoded_filter = request.query_params.get('filter', None)
#         decoded_filter = {}
#         try:
#             # Decode and parse the JSON filter
#             decoded_filter = json.loads(unquote(encoded_filter))
#         except:
#             decoded_filter = {}

#         print("decoded_filter",decoded_filter)

#         # Check if the decoded filter is a dictionary
#         if not isinstance(decoded_filter, dict):
#             decoded_filter={}

#         ResponseData=getUserByType(request.user,decoded_filter)
#         return Response(ResponseData)
    
#     except Exception as e:
#         print("Error", e)
#         error_response = {
#             'status': 500,
#             'error': 'something_went_wrong',
#             'message': 'Internal server error',
#             'data': {}
#         }
#         return Response(error_response, status=500)

