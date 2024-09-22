from django.shortcuts import render, redirect
from . import views
from cart.cart import Cart
from django.shortcuts import get_object_or_404
from payment.models import ShippingAddress
from payment.forms import ShippingForm, PaymentForm
from django.contrib import messages

def billing_info(request):
  if request.POST:
    cart = Cart(request) # Lấy giỏ hàng từ session hiện tại
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
      billing_form = PaymentForm()
      return render(request, "payment/billing_info.html",{'cart_products':cart_products, "quantities":quantities, "totals" : totals, "shipping_info": request.POST, "billing_form": billing_form})
    else:
      pass
      billing_form = PaymentForm()
    shipping_form = request.POST
    return render(request, "payment/billing_info.html",{'cart_products':cart_products, "quantities":quantities, "totals" : totals, "shipping_info": request.POST, "billing_form": billing_form})
  else:
    messages.success(request, "Access Denied")
    return redirect ('home')
def checkout(request):
  cart = Cart(request) # Lấy giỏ hàng từ session hiện tại
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()
  if request.user.is_authenticated:
    shipping_user = get_object_or_404(ShippingAddress, user=request.user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    return render(request, "payment/checkout.html",{'cart_products':cart_products, "quantities":quantities, "totals" : totals, "shipping_form": shipping_form})
  else:
    shipping_form = ShippingForm(request.POST or None)
    return render(request, "payment/checkout.html",{'cart_products':cart_products, "quantities":quantities, "totals" : totals,  "shipping_form": shipping_form})

def payment_success(request):
  return render(request, "payment/payment_success.html",{})
