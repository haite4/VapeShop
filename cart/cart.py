from django.conf import settings
from shop.models import Product
from decimal import Decimal

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self,product,quantity=1,update_quantity=False):
        product_slug = str(product.slug)
        if product_slug not in self.cart:
            self.cart[product_slug] = {"quantity":0,"price":str(product.final_price if product.discount else product.price)}
        if update_quantity:
            self.cart[product_slug]["quantity"] = quantity
        else:
            self.cart[product_slug]["quantity"] += quantity


        self.save()


    def save(self):
        self.session.modified = True


    
    def remove(self,product):
        product_slug = str(product.slug)
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    
    def __iter__(self):
        product_slugs = self.cart.keys()
        products =  Product.objects.filter(slug__in=product_slugs)


        cart = self.cart.copy()
        

        for product in products:
            cart[str(product.slug)]["product"] = product
        
        for item in cart.values():
            

            item["price"] = Decimal(item["price"])
            item["total_price"] = item["quantity"] * item["price"]
        
            yield item


    def __len__(self):
        return  sum(item["quantity"] for item in self.cart.values())
    

    def get_total_price(self):
        return sum(
            Decimal(item["price"])  * item["quantity"] for item in self.cart.values()
        )
    

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

        self.save()

















