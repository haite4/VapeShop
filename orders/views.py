from django.http import HttpResponse
from django.shortcuts import render,redirect
from orders.models import Order,OrderItem
from orders.forms import OrderForm
from cart.cart import Cart
import stripe
from django.conf import settings
from shop.models import Product
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from orders.models import UserPayment
from shop.recommender import Recommender
from account.models import AccountUser
from orders.tasks import order_created_mail
import uuid
# Create your views here.



stripe.api_key = settings.STRIPE_SECRET_KEY
    
    


    

@csrf_exempt
def create_checkout_session(request):
    server_domain =  "http://127.0.0.1:8000"
  
    cart = Cart(request)
    line_items = []

    for item in cart:
        product = item["product"] 
        quantity = item["quantity"]
        unit_amount = int(product.final_price * Decimal(100)) if hasattr(product, 'final_price') else int(product.price * Decimal(100))
        line_item = {
            "price_data": {
                "unit_amount": unit_amount,
                "currency": "eur",
                "product_data": {
                    "name": product.title,
                    
                },
               
                 
            },
            "quantity": quantity,
        
            
        }

        line_items.append(line_item)

   


    city =  request.POST["city"]
    postal_code = request.POST["postal_code"]
    adress = request.POST["adress"]
    email = request.POST["email"]
    firstName = request.POST["first_name"]
    lastName = request.POST["last_name"]


    customer = stripe.Customer.create(
        address={"city":city,"postal_code":postal_code,"line2":adress},
        email=email,
        name=f"{firstName} {lastName}",
        

    )
    

    checkout_session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    line_items=line_items,
    mode="payment",
    customer=customer,
    success_url=server_domain + "/checkout/success/?session_id={CHECKOUT_SESSION_ID}",
    cancel_url=server_domain +  "/checkout/canceled/?session_id={CHECKOUT_SESSION_ID}",
)

   
  
    return redirect(checkout_session.url, code=303)



def successpayment(request):
    cart  = Cart(request)
    session_id = request.GET.get("session_id",None)
    session = stripe.checkout.Session.retrieve(session_id)
    product_items = stripe.checkout.Session.list_line_items(
         session_id
    )
    cart_items = [ p["product"] for p in cart ]
   

    r = Recommender()
    r.product_bought(cart_items)

    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    adress = customer.address
    city = customer.address["city"]
    adress = customer.address["line2"]
    postal_code = customer.address["postal_code"]
    email = customer.email
    first_name = customer["name"].split(" ")[0]
    last_name = customer["name"].split(" ")[1]
#   
    if request.user.is_authenticated:
         
        user_payment = UserPayment.objects.get(user_app=user_id)
        user_payment.checkout_session_id = session.id

        user_payment.save()
        order = Order.objects.create(
            city = city,
            adress = adress,
            postal_code = postal_code,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_payment = user_payment,
            paid = True
    
        )
    else:
         request.session["nonuser"] = str(uuid.uuid4())
         user_payment,create = UserPayment.objects.get_or_create(session_id=request.session["nonuser"],anonymous_user_id=request.session["nonuser"])
         if create:
                order = Order.objects.create(
                city = city,
                adress = adress,
                postal_code = postal_code,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_payment = user_payment,
                paid = True,
        
            )   
                
    
    item_product_list = []
    for item in product_items.data:
        

            product = stripe.Product.retrieve(
            item.price.product
        )   
           
            orderitem = OrderItem.objects.create(
                product = Product.objects.get(title=product.name),
                order=order,
                name = product.name,
                unit_price = (item.price.unit_amount / Decimal(100)),
                quantity = item.quantity,
                amount_total = (session.amount_total / Decimal(100)),
                unit_amount = (item.price.unit_amount / Decimal(100)) *  item.quantity

            )
            
            purchase_product = Product.objects.get(title=product.name)
            purchase_product.quantity -=  item.quantity
            purchase_product.save()

            item_product_list.append(product.name)
    cart.clear()

    order_created_mail(order.id, product_name=item_product_list)

    return render(request, "orders/checkout/success-payment.html",{"customer":customer,
                                "order":order,"orderitem":orderitem})



def canceledpayment(request):
    
    return render(request,"orders/checkout/canceled-payment.html")



endpoint_secret = settings.ENDPOINT_SECRET 

@csrf_exempt
def my_webhook(request):
        payload = request.body
        stripe_signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None 
     
        

        try:
            event = stripe.Webhook.construct_event(
                 payload,stripe_signature_header,endpoint_secret
            )
        except stripe.SignatureVerificationError as e:
        

            print("Webhook signature verification failed", str(e))
            return HttpResponse(status=400)


     
     

     
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
           
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object # contains a stripe.PaymentMethod
          
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)
            



def checkoutpage(request):
        
        cart = Cart(request)
      
        if request.user.is_authenticated:
            account_info = AccountUser.objects.get(user=request.user)
            current_user = account_info.user

            ship_adress = account_info.ship_adress
            ship_postal_code = account_info.ship_postal_code
            ship_city = account_info.ship_city

            initial_data = {
                "city":ship_city,
                "adress":ship_adress,
                "postal_code":ship_postal_code,
                "first_name":current_user.first_name,
                "last_name":current_user.last_name,
                "email":current_user.email

            }
            
            
             
            form_data = OrderForm(
                initial=initial_data
            )
        else:
             form_data = OrderForm()
      
        return render(request,"orders/checkout/create.html", {"form":form_data,"cart":cart})

      
     


        








