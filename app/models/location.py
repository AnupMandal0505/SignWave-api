from django.db import models
from django.contrib.auth.models import User

class SavedAddress(models.Model):
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)  # Updated to OneToOneField
    address = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    lattitude = models.CharField(max_length=255)  # Optional: Consider renaming to 'latitude' for correct spelling
    longitude = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user_ref)

