from django.urls import path
from . import views

app_name = "account"


urlpatterns = [
    path("profile/", views.AccountProfileUser.as_view() ,name="account-main-page"),
    path("shipment_form_save/",views.AccountProfileUser.address_form_save, name="shipment-form"),
    path("change-email/", views.AccountProfileUser.change_email, name="change-email")
]