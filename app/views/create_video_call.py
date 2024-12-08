from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from app.models.create_call import CreateCall
from rest_framework.permissions import IsAuthenticated
from app.views.point import UsePoints
from app.models.point import PointRecord
from app.serializers.CreateCallSerializer import CreateCallSerializer
from app.views.otp import create_video_callte_mail,video_call_update_mail


permission_classes = [IsAuthenticated]  
class CreateCallAPI(APIView):
    def post(self, request):

        try:
            sender = request.user
            receiver = request.data.get('receiver')
            message = request.data.get('message', 'No message provided')            
            meetingtime = request.data.get('meetingtime')
            
            # Ensure all required fields are provided
            if not all([sender, receiver,meetingtime]):
                return Response(
                    {"message": "All fields are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_point_record = PointRecord.objects.filter(user_ref=request.user).first()
            print(user_point_record.balance)
            if user_point_record.balance < 5:
                return Response(
                    {
                        "message": "You have reached the maximum coin balance allowed. Please use some coins before buying more."
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)
            else: 

            
                # Check if user already exists
                try:
                    user = User.objects.get(username=receiver)
                    print(user)
                    createcall = CreateCall.objects.create(sender=sender, receiver=receiver, message=message,meetingtime=meetingtime)

                    UsePoints(user, receiver)
                    
                    # Optionally, use a serializer for validation (better practice)
                    # user_serializer = UserSerializer(user)
                    
                    create_video_callte_mail(request,user.email,user.first_name,meetingtime,sender.email,sender.first_name)
                    return Response(
                        {"message": 'Create call Successful!'}, 
                        status=status.HTTP_201_CREATED
                    )
                except ObjectDoesNotExist:
                    
                    return Response({"message": 'Invalid Id!'}, status=status.HTTP_400_BAD_REQUEST)

        
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


     
    def get(self,request):
        try:
            calls = CreateCall.objects.filter(sender=request.user)
            serializer = CreateCallSerializer(calls, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



    def put(self, request, id):
        """
        Update an existing call.
        """
        try:
            create_call = CreateCall.objects.get(id=id)  # Ensure the user is the sender
        except CreateCall.DoesNotExist:
            return Response({"error": "Call not found or unauthorized access."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateCallSerializer(create_call, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            up= serializer.save()
            us=User.objects.get(username=up.sender)
            print(up.meetingtime)
            video_call_update_mail(request,up.receiver,up.meetingtime,us.email,us.first_name)
            print(15466)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

