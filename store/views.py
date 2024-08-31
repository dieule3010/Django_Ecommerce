from django.shortcuts import render
from .models import Product
from .models import Category
from django.contrib.auth import authenticate, login, logout #Các hàm để quản lý xác thực người dùng (đăng nhập, đăng xuất, xác thực người dùng).
from django.contrib import messages #Để gửi thông báo cho người dùng.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.shortcuts import redirect #redirect: Hàm để chuyển hướng người dùng đến một URL khác.

def category(request,foo):
  foo = foo.replace('-', '') #Loại bỏ dấu - trong tên danh mục để chuẩn hóa giá trị.
  try:
    category = Category.objects.get(name=foo) #Tìm đối tượng Category với tên tương ứng. Nếu không tìm thấy, sẽ gây lỗi.
    products = Product.objects.filter(category=category) # Lọc các sản phẩm thuộc danh mục tìm được.
    return render(request,'category.html', {'products': products})
  except:
    messages.success(request,("That Category doesn't exist"))
    return redirect('home')

def product(request,pk): #pk: Primary key của sản phẩm cần lấy
  product = Product.objects.get(id=pk)
  return render(request, 'product.html',{'product': product})

def home(request):
  products = Product.objects.all()
  return render(request, 'home.html',{'products': products})

def about(request):
  return render(request, 'about.html',{})



def login_user(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        # Debug: In ra giá trị username và password
        print(f"Username: {user_name}, Password: {password}")

        if user_name and password:
            user = authenticate(request, username=user_name, password=password)
            # Debug: Kiểm tra nếu hàm authenticate trả về người dùng
            if user:
                print(f"Authenticated user: {user}")
            else:
                print("Failed to authenticate user")

            if user is not None:
                login(request, user)
                messages.success(request, "You're sucess")
                return redirect('home')
            else:
                messages.error(request, "Name and Password incorrect")
        else:
            messages.error(request, "You aren't fill out enough")

        return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
  logout(request)
  messages.success(request, ("You have been logged out...Thanks for stopping by..."))
  return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the form to create the user
            username = form.cleaned_data['username'] #Lấy tên người dùng từ dữ liệu đã được làm sạch.
            password = form.cleaned_data['password1']

            # Log in the user after registration
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You have registered successfully. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "There was a problem with registration.")
            return redirect('register')  # Redirect back to registration page if form is invalid
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})