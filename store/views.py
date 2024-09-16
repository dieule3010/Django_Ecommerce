from django.shortcuts import render
from .models import Product
from .models import Category
from .models import Profile
from django.contrib.auth import authenticate, login, logout #Các hàm để quản lý xác thực người dùng (đăng nhập, đăng xuất, xác thực người dùng).
from django.contrib import messages #Để gửi thông báo cho người dùng.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.shortcuts import redirect #redirect: Hàm để chuyển hướng người dùng đến một URL khác.
from django.db.models import Q
def search(request):
    # Check if the form was submitted via POST
    if request.method == "POST":
        # Retrieve the searched value from the form
        searched = request.POST.get('searched', '')
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains = search))
        if not searched:
            messages.success(request, "That product doesn't exist!!")
            return render(request, 'search.html', {})
        else:

        # Render the search results or whatever is needed
            return render(request, 'search.html', {'searched': searched})

    else:
        # Render the search form when it's not a POST request
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
      current_user = Profile.objects.get(user__id = request.user.id)
      form = UserInfoForm(request.POST or None, instance = current_user)
      if form.is_valid():
         form.save()
         login(request, current_user)
         messages.success(request, "Your Info Has Been Updated!!")
         return redirect('home')
      return render(request, 'update_info.html', {'form' : form})
    else:
         messages.success(request, "You Must Be Logged In to Access That Page!!")
         return redirect('home')

    return render(request, 'update_info.html', {})
def update_password(request):
    if request.user.is_authenticated: #kiểm tra xem người dùng hiện tại đã đăng nhập chưa. Nếu chưa đăng nhập, người dùng sẽ không được phép truy cập trang cập nhật mật khẩu và sẽ được chuyển hướng về trang chính (home).
        current_user = request.user
        if request.method == 'POST':#Kiểm tra xem yêu cầu HTTP là POST hay không. Yêu cầu POST là khi người dùng gửi dữ liệu form, trong trường hợp này là thông tin thay đổi mật khẩu.
            form = ChangePasswordForm(current_user, request.POST) #ChangePasswordForm(current_user, request.POST) khởi tạo form với dữ liệu từ yêu cầu POST. current_user được truyền vào để liên kết với người dùng hiện tại.
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been changed.")
                return redirect('login')
            else:
                for error in form.errors.values():  # Sửa lại cách lấy lỗi từ form
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(current_user) #Nếu yêu cầu không phải là POST (thường là GET), form sẽ được khởi tạo với đối tượng người dùng hiện tại mà không có dữ liệu POST. Sau đó, form sẽ được gửi đến template để hiển thị.
        return render(request, "update_password.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('home')


def update_user(request):
  if request.user.is_authenticated:
      current_user = User.objects.get(id = request.user.id)
      user_form = UpdateUserForm(request.POST or None, instance = current_user)
      if user_form.is_valid():
         user_form.save()
         login(request, current_user)
         messages.success(request, "User Has Been Updated!!")
         return redirect('home')
      return render(request, 'update_user.html', {'user_form' : user_form})
  else:
         messages.success(request, "You Must Be Logged In to Access That Page!!")
         return redirect('home')

  return render(request, 'update_user.html', {})

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
            return redirect('update_user')
        else:
            messages.error(request, "There was a problem with registration.")
            return redirect('register')  # Redirect back to registration page if form is invalid
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})