from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    # path('', views.home, name='home')
    path('adopt', views.adopt, name='adopt'),
    path('adopt/<int:trees_id>', views.specificTree, name='specificTree'),
    path('cart/<int:cart_id>', views.cartOperations, name='useCart'),
    path('cart/items/<int:in_cart_id>', views.inCartOperations, name='inCartOperations')
]
