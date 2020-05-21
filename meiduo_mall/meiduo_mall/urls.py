"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meiduo_admin/', include('meiduo_admin.urls')),
    path(r'', include('users.urls')),
    path(r'', include('verifications.urls')),
    path(r'', include('oatuh.urls')),
    path(r'', include('areas.urls')),
    path(r'', include('contents.urls')),
    path(r'', include('goods.urls')),
    path(r'', include('carts.urls')),
    path(r'', include('orders.urls')),
    path(r'', include('payment.urls')),
]
