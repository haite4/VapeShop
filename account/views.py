from typing import Any
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView
from account.models import AccountUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from django.contrib import messages
from orders.models import UserPayment,Order
from django.views.generic import View,TemplateView
from django.utils.decorators import method_decorator

from account.forms import ProfileUserForm,AccountShipUserForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# Create your views here.


     


class AccountProfileUser(View):


  

    @method_decorator(login_required(login_url="/auth/login/"))
    def get(self,request):
            account_user = AccountUser.objects.get(user=request.user)
            form = AccountShipUserForm(instance=account_user)
            
            emai_form = ProfileUserForm(instance=account_user)
            user_order = self.user_orders_info(self.request)
            return render(request, "account/pagemain-account.html", {"user_profile":account_user,
                                                                     "form":form,
                                                                     "user_order":user_order,
                                                                     "email_form":emai_form,
                                                                      })




    @method_decorator(login_required(login_url="/auth/login/"))
    def post(self,request):
         self.address_form_save(request)
        

    @staticmethod
    def address_form_save(request):
            if request.method == "POST":
                form = AccountShipUserForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    account_profile = get_object_or_404(AccountUser,user=request.user)

                    account_profile.ship_postal_code= cd["ship_postal_code"]
                    account_profile.ship_adress = cd["ship_adress"]
                    
                    
                    account_profile.ship_city = cd["ship_city"]
                    account_profile.save()
                    messages.success(request, "Adress succesfully save",extra_tags='adress_saved')
                    return redirect("account:account-main-page")
       

    def user_orders_info(self,request):
        current_user = request.user
        user_payment = UserPayment.objects.get(user_app=current_user)
        user_order = Order.objects.filter(user_payment=user_payment)
        print(user_order)
        return user_order
    

    @staticmethod
    @login_required
    def change_email(request):
        if request.method == "POST":
            form = ProfileUserForm(request.POST)
            
            if form.is_valid():

                cd = form.cleaned_data
                email = cd["email"]
                try:
                     validate_email(email)
                except ValidationError:
                        return redirect("account:account-main-page")
                customer = get_object_or_404(CustomUser,id=request.user.id)
                customer.email = email
                customer.save()


                return redirect("account:account-main-page")
        