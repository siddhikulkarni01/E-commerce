from django import forms
from ecomm.models import UserData
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password"]
        


class UserForm2(forms.ModelForm):

    class Meta:
        model = UserData
        fields = ["address","image"]

class Update1(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email"]

class Update2(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ["address","image"]

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)

