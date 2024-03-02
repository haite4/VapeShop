from typing import Any
from django.http import  JsonResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from shop.models import Category, Product,NotificationSubscription
from django.views import View
from django.shortcuts import get_object_or_404
from cart.forms import CartAddProductForm
from django.views.decorators.http import require_POST
from django.views.generic import ListView,DetailView
from shop.models import Reviews,Flavor,Brand,WishList,Fortress
from django.db.models import Q
from django.db.models import Min, Max
import json
from django.contrib.auth.decorators import login_required
from shop.recommender import Recommender
from shop.forms import NotificationSubscriptionForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.
import  ast
from django.db.models import Count
from django.core.paginator import Paginator
from datetime import datetime,timedelta
from  django.db.models import Avg
from django.views.generic import  TemplateView
from django.core.cache import cache
from django.conf import settings

class FilterProductAttribute:

     def get_flavor(self,category_slug):
          category = Category.objects.get(slug=category_slug)
          flavor = Flavor.objects.filter(category_id=category.id)
          return flavor
     
     

     def get_brand(self,category_slug):
          cateogory = Category.objects.get(slug=category_slug)
          brand = Brand.objects.filter(category_id=cateogory.id)
          return brand

     
     def get_fortress(self,category_slug):
          category = Category.objects.get(slug=category_slug)
          fortress = Fortress.objects.filter(category_id=category.id)
          return fortress

class ProductFiltebyprice:
    
    def filterproduct(request,slug):
          
          min_price = request.GET.get("price_min")
          max_price = request.GET.get("price_max")
         
          brand = request.GET.getlist("brand")
          flavor = request.GET.getlist("flavor")
          fortress = request.GET.getlist("fortress")
          
         
         
          if min_price is not None and max_price is not None:
               try:
                    category = Category.objects.get(slug=slug)
                 
                    products = Product.objects.filter(category=category, price__gte=min_price, price__lte=max_price)
                   
                    
                    if brand:
                         try:
                     
                              brand_ids = [int(b) for b in ast.literal_eval(brand[0])]
                              products = products.filter(brand__in=brand_ids)
                         except (ValueError, SyntaxError):
                              print("Invalid format for brand data")
                    else:
                         brand_ids = []

                    if flavor:
                         try:
                     
                              flavor_ids = [int(b) for b in ast.literal_eval(flavor[0])]
                              products = products.filter(flavor__in=flavor_ids)
                         except (ValueError, SyntaxError):
                              print("Invalid format for brand data")
                    else:
                         flavor_ids = []


                    
                    if fortress:
                         try:
                     
                              fortress_ids = [int(b) for b in ast.literal_eval(fortress[0])]
                              products = products.filter(fortress__in=fortress_ids)
                         except (ValueError, SyntaxError):
                              print("Invalid format for brand data")
                    else:
                         fortress_ids = []
                    

                  
                        
                   
                    data = render_to_string("products_items/price_filter_products.html", {"products": products})
                    return JsonResponse({"data": data})
               
               except Category.DoesNotExist:
                    return JsonResponse({"data": "Category not found"})
               except Exception as e:
                    return JsonResponse({"data": str(e)})
          
          return JsonResponse({"data": "No price range provided"})

   
class HomePageView(ListView):
     model = Product
     template_name = "products_items/home-page.html"
     queryset = Product.objects.all()




    
     def new_arrivals(request):
          interval = datetime.now() - timedelta(days=2)
          
          products = Product.objects.filter(
               Q(created_at__gte=interval),
               created_at__regex=r'^\d{4}-\d{2}-\d{2}'  
          )[:5]
          
          return products
     

     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          context["new_product"] = self.new_arrivals()
          context["product_discount"] = Product.objects.select_related("discount").filter(discount__active=True)

          return context




class ProductListView(FilterProductAttribute,ListView):
     model = Product
     queryset = Product.objects.select_related("discount").filter(active=True)
     template_name = 'products_items/products.html'
     context_object_name = "products"




     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context["page_obj"] = self.product_list()
          return context


     def product_list(self):
          cache_key = "product_list"
          queryset_cashe = cache.get(cache_key)

          if queryset_cashe:
               queryset = queryset_cashe
          else:
                    
               queryset = self.get_queryset()
               cache.set(cache_key, queryset, 10)
          pagination = Paginator(queryset, 25)

          page_number = self.request.GET.get("page")

          page_obj = pagination.get_page(page_number)
          
          return page_obj


class ProductDetailView(FilterProductAttribute,DetailView):
     model = Product
     slug_field = "slug"
     template_name = "products_items/product_detail.html"
     context_object_name = "product"
     slug_url_kwarg = "product_slug"


     def get_object(self):
          return get_object_or_404(Product, slug=self.kwargs.get("product_slug"))

     


     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          product = self.get_object()

          rating_key_cache = f'{settings.RATING_KEY_CACHE}_{product.pk}'
          cache_average_rating = cache.get(rating_key_cache)

          if cache_average_rating:
               average_rating = cache_average_rating
          else:
               average_rating = Reviews.objects.filter(product=product).aggregate(Avg("rate"))["rate__avg"]
               cache.set(rating_key_cache,average_rating,300)

          if average_rating is not None:
               round(average_rating,1)
               context["average_rating"] = average_rating
          
          context["review"] = Reviews.objects.filter(product=product)
          context["cart_product_form"] =  CartAddProductForm()
          context["recommender_products"] =  self.fetch_recommendations(product)
          context["form"] = NotificationSubscriptionForm()
      
    
         
          return context
     
   
     

     def fetch_recommendations(self,product):
          r=Recommender()
          product = product
          reccomend=r.suggest_product_for([product], 4)
        
          return reccomend
     



class ProductFilterView(FilterProductAttribute,ListView):
     model = Product
     template_name =  "products_items/category_products.html"
     context_object_name = "products_filter"
     slug_url_kwarg = "slug"

    
     def get_queryset(self):
          self.brand = self.request.GET.getlist("brand")
          self.flavor = self.request.GET.getlist("flavor")
          self.fortress = self.request.GET.getlist("fortress")
         
               
          querySet = Product.objects.filter(active=True,category__slug=self.kwargs.get("slug")).select_related("category")
         
          if self.brand:
          
               querySet = querySet.filter(brand__in=self.brand)

          if self.flavor:
               querySet = querySet.filter(flavor__in=self.flavor)

          
          if self.fortress:
               querySet = querySet.filter(fortress__in=self.fortress)

          
          return  querySet   
     

     def filterPrice(self):

          current_products = self.get_queryset()
        
          

          min_max_product = current_products.aggregate(price_min=Min("price"),price_max=Max("price"))
          
          return min_max_product
     
    

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
          context["category_slug"] = category.slug
          context["minmaxprice"] = self.filterPrice()
          if self.brand:
              
               context["brand"] =  self.brand
          brands_with_total_product = self.get_brands_with_total_products(category=category)
          context["brands"] = brands_with_total_product
          flavor = self.request.GET.getlist("flavor")
          if self.flavor:
               context["flavor"] = flavor
          flavor_with_total_product = self.get_flavors_with_total_products(category=category)
          context["flavors"] = flavor_with_total_product
          
          if self.fortress:
               context["fortres"] = self.fortress
          fortress_with_total_product = self.get_fortress_with_total_products(category=category)
          context["fortress"] = fortress_with_total_product
     
     
          return context

     
     def get_brands_with_total_products(self,category):
               brand_obj = Brand.objects.filter(product__category=category)
               brand_quantity = brand_obj.annotate(total_products=Count("product"))
         
               brand_quantity_list = [{"name":brand.name, 
                                       "total_products":brand.total_products,
                                       "id":brand.id } for brand in brand_quantity]
               
          
               return brand_quantity_list
     

     def get_flavors_with_total_products(self,category):
         
          flavor_obj = Flavor.objects.filter(product__category=category)
          flavor_quantity =  flavor_obj.annotate(total_products=Count("product"))
          flavor_quantity_list =[{"name":flavor.name, 
                                   "total_products":flavor.total_products,
                                   "id":flavor.id } 
                                   for flavor in flavor_quantity]
          

          return flavor_quantity_list
     


     def get_fortress_with_total_products(self,category):
         
          fortress_obj = Fortress.objects.filter(product__category=category)
          fortress_quantity =  fortress_obj.annotate(total_products=Count("product"))
          fortress_quantity_list =[{"name":fortress.strength, 
                                   "total_products":fortress.total_products,
                                   "id":fortress.id } 
                                   for fortress in fortress_quantity]
          

          return fortress_quantity_list
    
    

class AddReviews(View):
     

     def post(self,request,pk):
          user = request.user
          rating = request.POST.get("rating")
          email = request.POST.get("email")
          name = request.POST.get("name")
          text = request.POST.get("text")


          product = get_object_or_404(Product, id=pk)

          reviews = Reviews.objects.filter(user=user.id, product=product).exists()
          if not reviews:

               Reviews.objects.create(
               product=product,
               user=user,
               name=name,
               text=text,
               rate=rating,
               email=email

          )
          
          cache.delete(f"{settings.RATING_KEY_CACHE}_{product.pk}")
          
          

          return redirect("shop:product-detail", product.slug)
     

    



class SearchProduct(ListView):
     model = Product
     template_name =  "products_items/search-product.html"
     context_object_name = "products"


     def get_queryset(self):
          
          query = self.request.GET.get("q")
          return Product.objects.filter(title__icontains=query)
     
    

@login_required(login_url="/auth/login/")
def wishlist(request):
     wishlist = WishList.objects.filter(user=request.user)
     cart_add_product_form = CartAddProductForm(show_quantity_field=False)
     return render(request,"products_items/wishlist.html",{"wishlist":wishlist, "cart_add_product_form":cart_add_product_form})


@login_required
def add_to_wishlist(request):
     if request.method == "POST":
          product_id =  json.loads(request.body)
          product = get_object_or_404(Product,id=product_id)
          if product:
               if WishList.objects.filter(user=request.user, product=product):

                    return JsonResponse({"failed":"Product already in wishlist"})
               else:
               
                    WishList.objects.create(
                         user=request.user,
                         product=product
                    )
               return JsonResponse({"status":"product add to wishlist"})
          
          else:
               return JsonResponse({"status":"product not found"})


     return redirect("/")
     


@login_required
def remove_wishlist_item(request):
     if request.method == "POST":
          product_id = json.loads(request.body)
          product = get_object_or_404(Product,id=product_id)
          wishlistitem = WishList.objects.filter(user=request.user,product=product)
          if wishlistitem.exists():
               wishlistitem.delete()
               return JsonResponse({"status":"Product removed from wishlist"})
               
          else:
               return JsonResponse({"error":"Product not found"})
     
     return redirect("/")



def wishlistcount(request):
     if request.user.is_authenticated:

          count = WishList.objects.filter(user=request.user).count()

          return JsonResponse({"wishlist_count":count})               
     
     return JsonResponse({"error":"You dont have enough permission"})






@require_POST
def notify_me(request, product_slug):
     if request.method == 'POST':
          email = request.POST.get('email')
          name = request.POST.get("name")
          print(email)
          print(name)

          if not email or not name:
               return JsonResponse({"failed":"This fields cant be empty"})
          
          try:
               validate_email(email)
               
          except ValidationError :
               return JsonResponse({"failed":"Invalid email adress"})
       
     
        
          print("Email", email)
          product = get_object_or_404(Product, slug=product_slug)
          existing_subscription  = NotificationSubscription.objects.filter(product=product,user=request.user).exists()
          if existing_subscription:
               return JsonResponse({"failed":"You have already submitted this form"})
          else:

               notify = NotificationSubscription.objects.create(
                    user=request.user,
                    email=email,
                    name=name,
                    product=product

               )

               notify.save()
            

               return JsonResponse({'message': 'Email notification sent successfully.'})
          




class ContactsView(TemplateView):
     template_name = "products_items/contacts.html"
     


class ShipPaymentView(TemplateView):
     template_name = "products_items/ship_payment.html" 