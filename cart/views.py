from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
  cart = Cart(request) # Lấy giỏ hàng từ session hiện tại
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()
  return render(request, "cart_summary.html",{'cart_products':cart_products, "quantities":quantities, "totals" : totals})



def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))


        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Return response
        cart_quantity = cart.__len__()
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty ': cart_quantity})

        return response



def cart_delete(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
        # Get product_id and product_qty
      product_id = int(request.POST.get('product_id'))
        #Call delete function in Cart
      cart.delete(product = product_id)
      response = JsonResponse({'product': product_id})
      return response

# def cart_update(request):
#   cart = Cart(request)
#   if request.POST.get('action') == 'post':
#         # Get stuff
#         product_id = int(request.POST.get('product_id'))
#         product_qty = int(request.POST.get('product_qty'))
#         cart.update(product=product_id, quantity = product_qty)
#         response = JsonResponse({'qty': product_qty})
#         return response
#         # return redirect('cart_summary')
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product_id and product_qty
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        # Kiểm tra product_id và product_qty có giá trị hợp lệ không
        if product_id and product_qty and product_qty.isdigit():
            product_id = int(product_id)
            product_qty = int(product_qty)

            # Cập nhật giỏ hàng
            cart.update(product=product_id, quantity=product_qty)

            # Trả về phản hồi JSON
            response = JsonResponse({'qty': product_qty})
            return response
        else:
            # Trả về phản hồi lỗi nếu giá trị không hợp lệ
            return JsonResponse({'error': 'Invalid product_id or product_qty'}, status=400)

    # Nếu không phải yêu cầu POST với action 'post', có thể xử lý khác nếu cần
