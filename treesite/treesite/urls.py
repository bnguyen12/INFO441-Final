from django.contrib import admin
from django.urls import path, include
from main.views import showTreeData
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('', include('main.urls')),
    path('main/', include('main.urls')),
    path('treedata', showTreeData, name="treedata")
]