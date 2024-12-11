from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


TYPE_SUBSCRIPTION = (
    ("free", "free"),
    ("monthly", "monthly"),
    ("yearly", "yearly"),
)

class PointRecord(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=255)
    details = models.CharField(max_length=255,default="None")
    type_subscription = models.CharField(max_length=255,choices=TYPE_SUBSCRIPTION,default="free")
    left_call=models.CharField(max_length=20,default="5")
    date = models.DateTimeField(default=now)
    last_subscription_amount = models.DecimalField(max_digits=10,decimal_places=2,default=1.0)
    



    def __str__(self):
        return str(self.user_ref)
    
