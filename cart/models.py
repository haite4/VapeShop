from django.db import models
from users.models import CustomUser
from shop.models import Product
# Create your models here.



class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"   

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"   
