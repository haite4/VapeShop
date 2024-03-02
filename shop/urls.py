from django.urls import path
from .  import views




app_name="shop"
urlpatterns = [
    path("home/", views.HomePageView.as_view(), name="home-page"),
    path("product/",views.ProductListView.as_view(), name="product-page"),
    path("category/<slug:slug>/",views.ProductFilterView.as_view(),name="filter-category"),
    path("product-detail/<slug:product_slug>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("reviews/<int:pk>/", views.AddReviews.as_view(),name="review-add"),
    path("category/<slug:slug>/filter/", views.ProductFiltebyprice.filterproduct, name="filt"),
    path("search/",views.SearchProduct.as_view(), name="search-product"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_to_whishlist/", views.add_to_wishlist,name="addtowhishlist"),
    path("remove_wishlist_item/", views.remove_wishlist_item, name="remove_wishlist_item"),
    path("get_wishlist_count/",views.wishlistcount,name="wishlistcount"),
    path('product-detail/<slug:product_slug>/notify-me/', views.notify_me, name='notify_me'),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("ship_and_payment/", views.ShipPaymentView.as_view(),name="ship_payment")
     
   
]