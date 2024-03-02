from django.db import models
from users.models import CustomUser
from orders.models import Order
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.



class AccountUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    orders_info = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='user_orders', null=True, blank=True)
    ship_postal_code = models.CharField(max_length=20, blank=True,null=True)
    ship_adress = models.CharField(max_length=250,blank=True)
    ship_city = models.CharField(max_length=100,blank=True, null=True)

    @receiver(post_save, sender=CustomUser)
    def account_create(sender,instance,created,**kwargs):
        if created:
            AccountUser.objects.create(user=instance)





    def __str__(self):
        return f"{self.user}"