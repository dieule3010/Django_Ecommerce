from django.shortcuts import render
from .models import Product
from .models import Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.shortcuts import redirect

def category(request,foo):
  foo = foo.replace('-', '')
  try:
    category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=category)
    return render(request,'category.html', {'products: product'})
  except:
    messages.success(request,("That Category doesn't exist"))
    return redirect('home')

def product(request,pk):
  product = Product.objects.get(id=pk)
  return render(request, 'product.html',{'product': product})

def home(request):
  products = Product.objects.all()
  return render(request, 'home.html',{'products': products})

def about(request):
  return render(request, 'about.html',{})

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, "You have been logged in")
                    return redirect('home')
                else:
                    messages.error(request, "You do not have the necessary permissions to log in")
            else:
                messages.error(request, "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.")
        else:
            messages.error(request, "Username and password are required")

        return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
  logout(request)
  messages.success(request, ("You have been logged out...Thanks for stopping by..."))
  return redirect('home')

def register_user(request):
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      #log in user
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, ("You have Registered Successfully!!Welcome!"))
      return redirect('home')
    else:
      messages.success(request, ("Whoops!There was problem to register"))
      return redirect('register')

  else:
    return render(request,'register.html',{'form':form})