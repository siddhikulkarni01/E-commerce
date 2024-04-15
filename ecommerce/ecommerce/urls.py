"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from ecomm.views import *
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    # path('',index,name="index"),
    path('login/',user_login,name="login"),
    path('',home,name="home"),
    path('register',registration,name="registration"),
    path('logout/',user_logout,name="logout"),
    path('update',user_update,name="update"),
    path('admin/', admin.site.urls),
    path('profile/',profile,name="profile"),
    path('cart',view_cart,name="cart"),
    path('addtocart/<int:id>/',add_to_cart,name="addcart"),
    path('updatecart/',update_cart,name="update_cart"),
    path('checkout/',checkout,name="checkout"),
    path('placeorder/',placedorder,name="placedorder"),
    path('thankyou/',thankyou,name="thankyou"),
    path('remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('search/',search,name="search"),
    path('password-reset/', PasswordResetView.as_view(template_name = "password_reset.html"),name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name='password_reset_complete'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
