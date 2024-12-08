# serializers.py
from rest_framework import serializers
from app.models.location import SavedAddress

class SavedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAddress
        fields = ['address', 'district', 'pincode', 'state', 'country', 'lattitude', 'longitude', 'locality', 'user_ref']



    def update(self, instance, validated_data):
            # Ensure `sender` cannot be updated
            validated_data.pop('user_ref', None)
            return super().update(instance, validated_data)