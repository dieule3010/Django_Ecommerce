from django.shortcuts import render
from .models import Product

def home(request):
  products = Product.objects.all()
  return render(request, 'home.html',{'products': products})

def about(request):
  products = Product.objects.all()
  return render(request, 'about.html',{'products': products})