from django import forms
from .models import RentPayment


class RentPaymentForm(forms.ModelForm):

    class Meta:
        model = RentPayment
        fields = [
            "month_covered",
            "year",
            "amount",
            "date_paid",
            "is_paid",
            "remarks"
        ]