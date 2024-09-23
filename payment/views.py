from django.shortcuts import render, redirect
from . import views
from cart.cart import Cart
from django.shortcuts import get_object_or_404
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingForm, PaymentForm
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = False)
        return render(request, "payment/not_shipped_dash.html",{"orders": orders})
    else:
        messages.success(request, "Order Placed!")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = True)
        return render(request, "payment/shipped_dash.html",{"orders": orders})
    else:
        messages.success(request, "Order Placed!")
        return redirect('home')
def process_order(request):
    if request.POST:
      cart = Cart(request) # Lấy giỏ hàng từ session hiện tại
      cart_products = cart.get_prods
      quantities = cart.get_quants
      totals = cart.cart_total()
      payment_form = PaymentForm(request.POST or None)
      my_shipping = request.session.get('my_shipping')

      full_name = my_shipping['shipping_full_name']
      email = my_shipping['shipping_email']
      shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
      amount_paid = totals
      #Nếu người dùng đã đăng nhập (request.user.is_authenticated), đơn hàng sẽ được tạo
      if request.user.is_authenticated:
        user = request.user
        create_order = Order(user = user, full_name = full_name,email = email, shipping_address = shipping_address, amount_paid = amount_paid)
        create_order.save()
        messages.success(request, "Order Placed!")
        return redirect ('home')
      else:
        create_order = Order( full_name = full_name,email = email, shipping_address = shipping_address, amount_paid = amount_paid)
        create_order.save()
      #add order item
      #get the order id
        order_id = create_order.pk
        for product in cart_products():
          product_id = product.id
          if product.is_sale:
            price = product.sale_price
          else:
            price = product.price
          for key, value in quantities().items():
            if int(key) == product.id:
              create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price, )
              create_order_item.save()
        #delete our cart
        for key in list(request.session.keys()):
          if key == "session_key":
            del request.session[key]
        messages.success(request, "Order Placed!")
        return redirect ('home')
    else:
      messages.success(request, "Access Denied")
      return redirect ('home')



def billing_info(request):
  if request.POST:
    cart = Cart(request) # Lấy giỏ hàng từ session hiện tại
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping
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
