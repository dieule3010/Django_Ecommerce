from store.models import Product
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} #tao gio hang trong
        self.cart = cart
    def add(self, product,quantity):
        product_id = str(product.id) #Chuyển đổi ID của sản phẩm thành chuỗi để sử dụng làm khóa trong giỏ hàng (lưu trữ trong session dưới dạng dictionary).
        product_qty = str(quantity)
    # Logic
        if product_id in self.cart: #Kiểm tra xem sản phẩm đã có trong giỏ hàng hay chưa
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True # Đánh dấu session là đã thay đổi để đảm bảo rằng dữ liệu giỏ hàng mới sẽ được lưu lại.
    def __len__(self):
        return len(self.cart) #Trả về số lượng sản phẩm trong giỏ hàng.
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys() #Lấy tất cả các ID sản phẩm từ giỏ hàng.
        #use ids to look up product in database model
        products = Product.objects.filter(id__in=product_ids) # lọc các sản phẩm có ID nằm trong danh sách product_ids
        return products #Trả về queryset chứa các sản phẩm từ cơ sở dữ liệu.
    def get_quants(self):
        quantities =self.cart
        return quantities
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing
