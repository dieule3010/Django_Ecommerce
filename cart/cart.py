from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        product_qty = int(quantity)  # Chuyển quantity thành số nguyên

        if product_id in self.cart:
            self.cart[product_id] += product_qty  # Cập nhật số lượng nếu sản phẩm đã có trong giỏ
        else:
            self.cart[product_id] = product_qty  # Thêm sản phẩm mới vào giỏ

        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())  # Số lượng tổng các sản phẩm trong giỏ

    def get_prods(self):
        product_ids = self.cart.keys()  # Lấy tất cả ID sản phẩm từ giỏ
        products = Product.objects.filter(id__in=product_ids)  # Tìm sản phẩm trong cơ sở dữ liệu
        return products

    def get_quants(self):
        return self.cart  # Trả về số lượng sản phẩm trong giỏ
