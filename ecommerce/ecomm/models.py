from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone

# Create your models here.
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return self.user.username



class Category(models.Model):

    category =  models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category

class Productdata(models.Model):

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product/',blank=True,null=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class Order(models.Model):

    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Productdata, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
    address = models.CharField(max_length=100, default='', blank=True) 
    phone = models.CharField(max_length=100, default='', blank=True) 
    date = models.DateTimeField(auto_now_add=True) 
    status = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.product)
    
    def multiply(self):
        return self.quantity * self.price

    def placeorder(self):
        self.save()


    @staticmethod
    def get_customer_user(id):
        return Order.objects.filter(user=id).order_by('-date')


class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Productdata, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
    address = models.CharField(max_length=100, default='', blank=True) 
    phone = models.CharField(max_length=100, default='', blank=True) 
    date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the order is created
    status = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.product)

    def total_price(self):
        return self.quantity * self.price