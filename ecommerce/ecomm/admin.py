from django.contrib import admin
from .models import UserData,Productdata,Order,Category,UserOrder
# Register your models here.

admin.site.register(UserData)
admin.site.register(Productdata)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(UserOrder)
