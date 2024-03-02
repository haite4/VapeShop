from django import forms
from shop.models import Reviews,NotificationSubscription





class ReviewsForms(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("name","email","text")






class NotificationSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NotificationSubscription
        fields  = ("name","email")