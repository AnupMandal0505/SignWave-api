from rest_framework.serializers import ModelSerializer
from app.models import User
# from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # exclude = ['last_name']
        fields = '__all__'

