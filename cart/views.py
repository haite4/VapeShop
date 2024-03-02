from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Product,Category,Discount
from .cart import Cart
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
from shop.recommender import Recommender
# Create your views here.


@require_POST
def cart_add(request,product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product,slug=product_slug)
    

    form =  CartAddProductForm(request.POST)
    if form.is_valid():
        item = form.cleaned_data

        cart.add(
        product=product,
        quantity=item["quantity"],
        update_quantity=item["update"],
        )
              
    return redirect("cart:cart-detail")

    

def cart_remove(request,product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product,slug=product_slug)
    cart.remove(product=product)
    return redirect("cart:cart-detail")





def cart_detail(request):
    cart = Cart(request)
    cart_products = []
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={"quantity":item["quantity"],"update":True}
        )
        cart_products.append(item["product"])
    r = Recommender()
       
    recommender_products = r.suggest_product_for(product=cart_products,max_result=4)

    return render(request, "cart/detail.html", {"cart":cart, "recommender_products":recommender_products})

