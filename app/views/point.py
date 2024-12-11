from app.models.point import PointRecord
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from app.serializers.PointSerializer import PointSerializer
from rest_framework.response import Response
from rest_framework import status
from app.views.otp import payment



def UsePoints(request,receiver):
    try:
        print(request.user,receiver)
        username=request.user
        user_point_record = PointRecord.objects.filter(user_ref=request.user).first()

        print("mlk",user_point_record)
        # left_calls = max(0,user_point_record.left_call-1)
        left_calls=int(user_point_record.left_call) - 1
        user_point_record.left_call=left_calls
        user_point_record.save()
        # balance = max(0,user_point_record.balance - 5)
        # bonus = max(0,user_point_record.bonus - 5)

        details=f"use 1 call remian {left_calls} call left"
        # print(details)


        # user_point_record.balance = balance
        # user_point_record.bonus = bonus
        # user_point_record.save()


        print(left_calls)
        
        PointRecord.objects.create(user_ref=username, receiver=receiver, details=details, left_call=str(left_calls), type_subscription=user_point_record.type_subscription,last_subscription_amount=user_point_record.last_subscription_amount)
        print(156235626526623)
    except PointRecord.DoesNotExist:
        print(f"Error: PointRecord does not exist for user {username}")
        raise Exception("User's PointRecord not found!")




def AfterPayment(request,username, transaction_amount,payment_id,email,name):
    try:
        user_point_record = PointRecord.objects.filter(user_ref=username).first()
        print(user_point_record)
        print(username)
        print(transaction_amount)
        print(payment_id)
        print(email)
        print(name)

        if transaction_amount == 50:
            type_subscription="monthly"
            left_call=12
        elif transaction_amount == 100:
            type_subscription="yearly"
            left_call=30

        print(type_subscription)
        print(type(left_call))
        last_subscription_amount = user_point_record.last_subscription_amount + transaction_amount
        user_point_record.last_subscription_amount = last_subscription_amount
        user_point_record.save()
        left_call = int(user_point_record.left_call) + left_call
        user_point_record.left_call = left_call
        user_point_record.save()

        # user_point_record.save()

        details = f"{transaction_amount} Paid"
        receiver = "Online payment"
        PointRecord.objects.create(user_ref=username, receiver=receiver, details=details, left_call=str(left_call), type_subscription=type_subscription,last_subscription_amount=transaction_amount)

        
        payment(request,email,name,transaction_amount,payment_id,user_point_record.left_call)
    except PointRecord.DoesNotExist:
        print(f"Error: PointRecord does not exist for user {username}")
        raise Exception("User's PointRecord not found!")







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PointRecords(request):
    precord = PointRecord.objects.filter(user_ref=request.user)
        
    serializer = PointSerializer(precord, many=True)

    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)
