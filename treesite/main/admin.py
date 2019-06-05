from django.contrib import admin

# Register your models here.
from .models import TreeType, Trees, UserTrees, Cart, InCart, Permissions, UserPosts

admin.site.register(TreeType)
admin.site.register(Trees)
admin.site.register(UserTrees)
admin.site.register(Cart)
admin.site.register(InCart)
admin.site.register(Permissions)
admin.site.register(UserPosts)