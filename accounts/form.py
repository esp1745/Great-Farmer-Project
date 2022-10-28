from dataclasses import field
from typing_extensions import Required
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Post,User, Product,Farmer,Customer
from django import forms
from django.core.validators import RegexValidator
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields


class FarmerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True,)
 
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name','email','phone_number','is_farmer')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_farmer'].widget.attrs.update({'type':'checkbox', 'class':'form-check-input','id':'lexCheckChecked'})
        
class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    # customer_type = forms.CharField(required=True)

    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name','email','phone_number','is_customer')
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_customer'].widget.attrs.update({'type':'checkbox', 'class':'form-check-input','id':'lexCheckChecked'})
        
class productsForm(ModelForm):
    class Meta:
        model = Product
        fields =['product_name', 'price']
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'type':'text', 'class':'form-control', 'id':'recipient-name'})
        self.fields['price'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        
class RateForm(forms.ModelForm):
    # rate = forms.ChoiceField(choices=RATE_CHOICE, widget=forms.Select(),required=True)
    # farmer = form
    class Meta:
        model = Farmer
        fields = ['rate']
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields =['title','description','price', 'product']
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        self.fields['description'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        self.fields['price'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        self.fields['product'].widget.attrs.update({'type':'text', 'class':'form-control', 'id':'recipient-name'})
        # self.fields['farmer'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})

class MapFormFarmer(ModelForm):
    latitude=forms.DecimalField(required=True)
    longitude=forms.DecimalField(required=True)
    
    class Meta(UserCreationForm):
        model=Farmer
        fields=['latitude','longitude']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs.update({'type':'number', 'class':'form-control','name':'latitude' , 'id':'recipient-name'})
        self.fields['longitude'].widget.attrs.update({'type':'number', 'class':'form-control','name':'latitude', 'id':'recipient-name'})

class MapFormCustomer(ModelForm):
    latitude=forms.DecimalField(required=True)
    longitude=forms.DecimalField(required=True)
    
    class Meta(UserCreationForm):
        model=Customer
        fields=['latitude','longitude','customer_price','customer_rating']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs.update({'type':'number', 'class':'form-control','name':'latitude' , 'id':'recipient-name'})
        self.fields['longitude'].widget.attrs.update({'type':'number', 'class':'form-control','name':'latitude', 'id':'recipient-name'})


class UserProfile(ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','phone_number']
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].widget.attrs.update({'type':'text', 'class':'form-control', 'id':'recipient-name','name':'first_name'})
            self.fields['last_name'].widget.attrs.update({'type':'text', 'class':'form-control','name':'last_name', 'id':'recipient-name'})
            self.fields['email'].widget.attrs.update({'type':'email', 'class':'form-control','name':'email', 'id':'recipient-name'})
            self.fields['phone_number'].widget.attrs.update({'type':'text', 'class':'form-control','name':'phone_number', 'id':'recipient-name'})


# class CustomerProfile(ModelForm):
#     class Meta:
#         model=Customer
#         fields=['customer_price','customer_rating']