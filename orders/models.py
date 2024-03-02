from django.db import models
from users.models import CustomUser
from shop.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class UserPayment(models.Model):
    user_app = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True)
    checkout_session_id = models.CharField(max_length=500)
    session_id = models.CharField(max_length=100)
    anonymous_user_id = models.CharField(max_length=100, blank=True, null=True)
    


    def __str__(self):
        return f"{self.checkout_session_id}-{self.user_app}"
    


    @receiver(post_save,sender=CustomUser)
    def create_user_payment(sender,instance,created,**kwargs):
        if created:
            UserPayment.objects.create(user_app=instance)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    adress = models.CharField(max_length=250)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    user_payment = models.ForeignKey(UserPayment,on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id}"


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Order"
        verbose_name_plural = "Orders"   







class OrderItem(models.Model):
    name = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_amount = models.DecimalField(max_digits=10,decimal_places=2)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.id}"


    def get_cost(self):
        return self.price * self.unit_price

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"   