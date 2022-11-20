from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"), # home page
    path('product_details/<int:pk>', views.product_details, name="product_details"), # product details page
    path('category_products/<int:pk>', views.category_products, name="category_products"), # search products by category
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
]