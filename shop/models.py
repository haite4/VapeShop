from django.db import models
from django.urls import reverse
from users.models import CustomUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100,unique=True)


    def __str__(self):
        return self.slug 
    
    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"    


class Fortress(models.Model):
    strength=models.IntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



    def __str__(self):
        return str(self.strength)

class Flavor(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    

class Discount(models.Model):
    name = models.CharField(max_length=250)
    active = models.BooleanField(default=False)

    amount = models.DecimalField(max_digits=10,decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()


    


    def __str__(self):
        return f"{self.name} - {self.amount} "


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/",blank=True)
    quantity = models.PositiveIntegerField(default=1)
    active= models.BooleanField(default=True)
    flavor = models.ManyToManyField(Flavor,blank=True)
    brand = models.ManyToManyField(Brand,blank=True)
    fortress = models.ManyToManyField(Fortress,blank=True)
    discount = models.OneToOneField(Discount,null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"   

    def __str__(self):
        return self.title


    @property
    def final_price(self):
        current_time = timezone.localtime(timezone.now())
        if self.discount and self.discount.active and self.discount.start_date <= current_time <= self.discount.end_date:
            discount_percent = self.discount.amount
            discount_amount = (self.price *  discount_percent) / 100
            return self.price - discount_amount
        else:
            self.discount.active = False
            self.discount.save()
            return self.price

class WishList(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="user_whishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products_whishlist")

    class Meta:
        ordering = ("-id",)
   
class LikedProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userlike")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productlike")
    created_at = models.DateTimeField(auto_now_add=True)


    
    def __str__(self):
        return f"{self.user.username} likes {self.product.title}"
    





class Reviews(models.Model):
    name = models.CharField(max_length=150,blank=False)
    email = models.EmailField(max_length=155,blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="review")
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering = ("-id",)

    def __str__(self):
        return f"{self.name} - {self.product}"






    






class NotificationSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=False)
    name = models.CharField(max_length=50,blank=False)
    email = models.EmailField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    notification_sent = models.BooleanField(default=False)





    def __str__(self):
        return f"{self.email}"