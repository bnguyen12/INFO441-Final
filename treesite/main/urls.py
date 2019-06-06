from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.loadoptions, name="loadoptions"),
    path('explore', views.exploreView, name="exploreView"),
    path('explore/<int:post_id>', views.exploreDeletePost, name="exploreDeletePost"),
    path('explore/makeapost', views.exploreMakeAPost, name="exploreMakeAPost"),
    path('profile', views.userProfileView, name="userProfileView"),
    path('profile/edit', views.userProfileEdit, name="userProfileEdit"),
    path('adminview', views.adminView, name="adminView"),
    path('admindeletepost/<int:post_id>', views.adminDeletePost, name="adminDeletePost"),
    path('admindeleteuser/<int:user_id>', views.adminDeleteUser, name="adminDeleteUser"),
    path('adopt', views.adopt, name='adopt'),
    path('adopt/<int:trees_id>', views.specificTree, name='specificTree'),
    path('cart', views.cartOperations, name='useCart'),
    path('cart/items/<int:in_cart_id>', views.inCartOperations, name='inCartOperations'),
    path('scrape', views.scrapeData, name='scrape'),
    path('contactus', TemplateView.as_view(template_name='main/contactus.html'), name='contactus'),
    path('aboutus', TemplateView.as_view(template_name='main/aboutus.html'), name='aboutus'),
    path('displayplants', views.displayPlantAPI, name='displayplants')
]
