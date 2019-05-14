from django.contrib import admin

# Register your models here.
from .models import TreeType, Trees, TreeAddress, UserTrees, Cart, InCart, permissions, user_posts

admin.site.register(TreeType)
admin.site.register(Trees)
admin.site.register(TreeAddress)
admin.site.register(UserTrees)
admin.site.register(Cart)
admin.site.register(InCart)
admin.site.register(permissions)
admin.site.register(user_posts)