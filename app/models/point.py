from django.db import models
from django.contrib.auth.models import User
 

POINT_STATUS = (
    ("add coins", "add coins"),
    ("success", "success"),
)

class PointRecord(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=POINT_STATUS)
    details = models.CharField(max_length=255,)
    date = models.DateTimeField(auto_now_add=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=100.0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)



    def __str__(self):
        return str(self.user_ref)
    
