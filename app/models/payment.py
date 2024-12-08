from django.db import models
from django.contrib.auth.models import User

STATUS = (
    ("Failed", "Failed"),
    ("Success", "Success"),
    ("None", "None"),
)

class PaymentRecord(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    payment_id = models.CharField(max_length=25, unique=True, default=None)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        # Return the `payment_id` or another existing field for display purposes
        return f"Payment ID: {self.payment_id}, Status: {self.status}"

