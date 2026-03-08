from django.contrib import admin
from django.urls import path
from payments import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard, name='dashboard'),

    path('add/', views.add_payment, name='add_payment'),
]
path('report/', views.rent_report_pdf, name='rent_report_pdf'),