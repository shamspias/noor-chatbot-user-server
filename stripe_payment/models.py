from django.db import models
from django.utils import timezone

from ausers.models import User


class Subscription(models.Model):
    """
    Model to Maintain subscription
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the subscription has ended
        if self.end_date < timezone.now().date() and self.payment_status:
            # Set payment status to False
            self.payment_status = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subscription_plan
