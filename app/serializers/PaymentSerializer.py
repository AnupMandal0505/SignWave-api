from rest_framework.serializers import ModelSerializer
from app.models.payment import PaymentRecord

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = PaymentRecord
        # exclude = ['user_ref', 'receiver', 'status','details', 'date', 'bonus','balance']
        fields = '__all__'

