from django.contrib import admin
from shop.models import Category, Product,LikedProduct,Flavor,Brand,Fortress
from django.utils.safestring import mark_safe
from shop.models import Discount,NotificationSubscription,Reviews
# Register your models here.





class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fields = ["name","slug"]
    prepopulated_fields = {"slug":("name",)}
    list_display = ("name",)
    search_fields = ["name","slug"]

class FlavorAdmin(admin.ModelAdmin):
    model = Flavor
    list_display = ("name",)

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ("name",)


class FortressAdmin(admin.ModelAdmin):
    model = Flavor
    list_display= ("strength",)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["title","description",
                    "price","category","quantity","get_image","created_at","updated_at"]
    search_fields = ["title","price","description"]
    prepopulated_fields = {"slug":("title",)}
    readonly_fields = ("get_image",)
   


 

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width='50px' height='50px'>")
        return ""
    get_image.short_description = "Image"


class LikedProductAdmin(admin.ModelAdmin):
    model = LikedProduct



class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews




class DiscountAdmin(admin.ModelAdmin):
    model = Discount



class NotificationSubscriptionAdmin(admin.ModelAdmin):
    model = NotificationSubscription

admin.site.register(Fortress,FortressAdmin)
admin.site.register(NotificationSubscription, NotificationSubscriptionAdmin)
admin.site.register(Flavor,FlavorAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(LikedProduct,LikedProductAdmin )
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Discount,DiscountAdmin)
admin.site.register(Reviews,ReviewsAdmin)