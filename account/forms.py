from django import forms
from account.models import AccountUser
from users.models import CustomUser







class AccountShipUserForm(forms.ModelForm):
    class Meta:
        model = AccountUser
        fields = ("ship_postal_code","ship_adress","ship_city")




class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email",)