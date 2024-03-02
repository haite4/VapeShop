from django.urls import path
from . import views


app_name = "order"

urlpatterns = [
    path("", views.checkoutpage,name="checkout"),
    path("payment/",views.create_checkout_session,name="payment"),
    path("success/", views.successpayment,name="success-payment"),
    path("canceled/",views.canceledpayment,name="canceled-payment"),
   
]