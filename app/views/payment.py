from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models.payment import PaymentRecord
from rest_framework.permissions import IsAuthenticated
from app.views.point import AfterPayment  # Import the AddValue function
from app.serializers.PaymentSerializer import PaymentSerializer


class PaymentAPI(APIView):
    permission_classes = [IsAuthenticated]  # Correct placement of permission

    def post(self, request):
        try:
            user_ref = request.user
            payment_id = request.data.get('payment_id')
            transaction_amount = request.data.get('transaction_amount')
            
            
            if not user_ref or not payment_id or not transaction_amount:
                return Response(
                    {'status': 400, 'error': 'missing_fields', 'message': 'Missing required fields', 'data': {}},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new payment record
            PaymentRecord.objects.create(user_ref=user_ref, payment_id=payment_id, transaction_amount=transaction_amount, status="Success")

            AfterPayment(request,user_ref,transaction_amount,payment_id,request.user.email,request.user.first_name)
            return Response(
                {"message": 'Payment Successful!'},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"Error: {e}")
            
            return Response(
                {
                    'status': 400,
                    'error': 'something_went_wrong',
                    'message': 'An error occurred during the payment process.',
                    'data': {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )



    def get(self, request):
        payment_data = PaymentRecord.objects.filter(user_ref=request.user)
        
        serializer = PaymentSerializer(payment_data, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)