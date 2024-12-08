from app.models.point import PointRecord
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from app.serializers.PointSerializer import PointSerializer
from rest_framework.response import Response
from rest_framework import status
from app.views.otp import payment



def UsePoints(username,receiver):
    try:
        user_point_record = PointRecord.objects.filter(user_ref=username).first()

        balance = max(0,user_point_record.balance - 5)
        bonus = max(0,user_point_record.bonus - 5)

        if user_point_record.bonus == 0:
            details = f"Use 10 coins Wallet"
        else:
            details = f"Use Bonus 5 And 5 Wallet"



        user_point_record.balance = balance
        user_point_record.bonus = bonus
        user_point_record.save()



        
        PointRecord.objects.create(
            user_ref=username, receiver=receiver, status="success", details=details, bonus=bonus, balance=balance
        )

    except PointRecord.DoesNotExist:
        print(f"Error: PointRecord does not exist for user {username}")
        raise Exception("User's PointRecord not found!")




def AfterPayment(request,username, transaction_amount,payment_id,email,name):
    try:
        user_point_record = PointRecord.objects.filter(user_ref=username).first()

        balance = user_point_record.balance + transaction_amount
        bonus = user_point_record.bonus

        user_point_record.balance = balance
        user_point_record.save()

        details = f"{transaction_amount} Paid"
        receiver = "Online payment"
        PointRecord.objects.create(
            user_ref=username, receiver=receiver, status="success", details=details, bonus=bonus, balance=balance
        )
        payment(request,email,name,transaction_amount,payment_id,user_point_record.balance)
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
