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
    path('admindeletepost', views.adminDeletePost, name="adminDeletePost"),
    path('admindeleteuser', views.adminDeleteUser, name="adminDeleteUser")
]
