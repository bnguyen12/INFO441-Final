from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('explore', views.exploreView, name="exploreView"),
    path('explore/<int:post_id>', views.exploreDeletePost, name="exploreDeletePost"),
    path('explore/makepost', views.exploreMakeAPost, name="exploreMakeAPost"),
    path('profile', views.userProfileView, name="userProfileView"),
    path('profile/edit', views.userProfileEdit, name="userProfileEdit"),
    path('adminview', views.adminView, name="adminView"),
    path('admindeletepost/<int:post_id>', views.adminDeletePost, name="adminDeletePost"),
    path('admindeleteuser/<int:user_id>', views.adminDeleteUser, name="adminDeleteUser"),
    path('adopt', views.adopt, name='adopt'),
    path('adopt/<int:trees_id>', views.specificTree, name='specificTree'),
    path('cart/<int:cart_id>', views.cartOperations, name='useCart'),
    path('cart/items/<int:in_cart_id>', views.inCartOperations, name='inCartOperations')
]
