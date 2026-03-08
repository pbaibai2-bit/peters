from django.db import models
from django.utils import timezone


class RentPayment(models.Model):
    month_covered = models.CharField(max_length=20)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.month_covered} {self.year} - K{self.amount}"