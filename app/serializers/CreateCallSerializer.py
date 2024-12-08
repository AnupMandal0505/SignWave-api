from rest_framework.serializers import ModelSerializer
# from rest_framework import serializers
from app.models.create_call import CreateCall



class CreateCallSerializer(ModelSerializer):
    class Meta:
        model = CreateCall
        # exclude = ['password', 'id', 'last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions']
        fields = '__all__'


    def update(self, instance, validated_data):
        # Ensure `sender` cannot be updated
        validated_data.pop('sender', None)
        return super().update(instance, validated_data)