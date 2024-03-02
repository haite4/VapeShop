from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order
from orders.models import OrderItem
from django.conf import settings
from shop.models import Product



@shared_task
def order_created_mail(order_id, product_name):
    print(product_name)
    order = Order.objects.get(id=order_id)
    product =  Product.objects.filter(title__in=product_name)
    print(product)
    result_product_title = []
    for item in product:
        product_title = item.title
        print("Product title",product_title)
        result_product_title.append(product_title)
 

    subject = f"Order:{order.id}"
    message = f"Dear {order.first_name}, You have succesfully placed an order.\
                                        Your order id is {order.id}. \n  \n Your purchase:  {', '.join(result_product_title)}  \n \n \
                                        Your item will be delivered within 1 week"

    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email]
    )

    return mail_sent



