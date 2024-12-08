from django.db import models
from django.contrib.auth.models import User



class CreateCall(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=10,blank=False)
    message = models.CharField(max_length=25,default=None)
    meetingtime = models.DateTimeField()  # Users set this manually
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets when the record is created
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.sender)

