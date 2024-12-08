from rest_framework.serializers import ModelSerializer
from app.models.point import PointRecord

class PointSerializer(ModelSerializer):
    class Meta:
        model = PointRecord
        # exclude = ['user_ref', 'receiver', 'status','details', 'date', 'bonus','balance']
        fields = '__all__'

