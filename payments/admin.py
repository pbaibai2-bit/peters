from django.contrib import admin
from .models import RentPayment


@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ("month_covered", "year", "amount", "is_paid", "date_paid")
    list_filter = ("year", "is_paid")
    search_fields = ("month_covered",)