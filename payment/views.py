from django.shortcuts import render
from . import views

def payment_success(request):
  return render(request, "payment/payment_success.html",{})
