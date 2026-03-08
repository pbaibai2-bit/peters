from django.shortcuts import render
from .models import RentPayment
from django.db.models import Sum
from datetime import datetime


def dashboard(request):

    payments = RentPayment.objects.all().order_by("-year")

    total_paid = RentPayment.objects.filter(is_paid=True).aggregate(Sum("amount"))["amount__sum"] or 0

    monthly_rent = 3000
    current_month = datetime.now().month
    expected_rent = current_month * monthly_rent

    difference = total_paid - expected_rent
    abs_difference = abs(difference)   # NEW LINE

    return render(request, 'payments/dashboard.html', {

    'payments': payments,
    'monthly_rent': monthly_rent,
    'total_paid': total_paid,
    'expected_rent': expected_rent,
    'difference': difference,
    'abs_difference': abs_difference,

    'total_rent_year': total_rent_year,
    'months_paid': months_paid,
    'months_total': months_total,
    'outstanding_rent': outstanding_rent,
    'payment_trend': payment_trend
})

from datetime import datetime

current_year = datetime.now().year

year_payments = RentPayment.objects.filter(year=current_year)

total_rent_year = sum(p.amount for p in year_payments)

months_paid = year_payments.filter(is_paid=True).count()

months_total = year_payments.count()

outstanding_rent = sum(p.amount for p in year_payments if not p.is_paid)

payment_trend = "Good"

if outstanding_rent > 0:
    payment_trend = "Needs Attention"
     
    return render(request, "payments/dashboard.html", context)
from .forms import RentPaymentForm
from django.shortcuts import redirect


def add_payment(request):

    if request.method == "POST":
        form = RentPaymentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = RentPaymentForm()

    return render(request, "payments/add_payment.html", {"form": form})
    from django.http import HttpResponse
from reportlab.pdfgen import canvas

def rent_report_pdf(request):

    payments = RentPayment.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rent_report.pdf"'

    p = canvas.Canvas(response)

    p.drawString(200, 800, "Rent Payment Report")

    y = 750

    for payment in payments:
        line = f"{payment.month_covered} {payment.year} - K{payment.amount} - {'Paid' if payment.is_paid else 'Pending'}"
        p.drawString(100, y, line)
        y -= 20

    p.showPage()
    p.save()

    return response

from django.shortcuts import get_object_or_404, redirect


def edit_payment(request, id):

    payment = get_object_or_404(RentPayment, id=id)

    if request.method == "POST":
        payment.month_covered = request.POST['month']
        payment.year = request.POST['year']
        payment.amount = request.POST['amount']
        payment.date_paid = request.POST['date_paid']
        payment.remarks = request.POST['remarks']

        payment.is_paid = 'is_paid' in request.POST

        payment.save()

        return redirect('dashboard')

    return render(request, 'payments/edit_payment.html', {'payment': payment})

def delete_payment(request, id):

    payment = get_object_or_404(RentPayment, id=id)

    payment.delete()

    return redirect('dashboard')

from datetime import datetime
from django.shortcuts import redirect

def generate_months(request):

    current_year = datetime.now().year

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    for month in months:

        exists = RentPayment.objects.filter(
            month_covered=month,
            year=current_year
        ).exists()

        if not exists:
            RentPayment.objects.create(
                month_covered=month,
                year=current_year,
                amount=0,
                is_paid=False
            )

    return redirect('dashboard')