from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User  # Use Django's default User model
# from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'id', 'last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions']
        # fields = '__all__'

