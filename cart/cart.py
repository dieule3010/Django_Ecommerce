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
    def cart_total(self):
        #get product_ids
        product_ids = self.cart.keys()
        #look up those keys in our products database models
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        #start counting at 0
        total = 0
        for key, value in quantities.items():
            #convert kew strings into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total
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
        product_id = str(product) # Chuyển đổi ID sản phẩm thành chuỗi
        product_qty = int(quantity) # Đảm bảo số lượng là kiểu số nguyên
        ourcart = self.cart# Lấy giỏ hàng hiện tại
        ourcart[product_id] = product_qty# Cập nhật giỏ hàng với số lượng mới của sản phẩm
        self.session.modified = True# Đánh dấu session đã được sửa đổi để lưu thay đổi
        thing = self.cart# Tùy chọn lưu giỏ hàng cập nhật vào 'thing'
        return thing # Trả về giỏ hàng đã cập nhật
    def delete(self, product):
        product_id = str(product)# Chuyển đổi ID sản phẩm thành chuỗi
        if product_id in self.cart:# Kiểm tra xem sản phẩm có tồn tại trong giỏ hàng không
            del self.cart[product_id]# Xóa sản phẩm khỏi giỏ hàng
        self.session.modified = True# Đánh dấu session đã được sửa đổi để lưu thay đổi
