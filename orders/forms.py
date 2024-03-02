from orders.models import Order
from django import forms




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name","last_name","postal_code",
                  "adress","email","city"]