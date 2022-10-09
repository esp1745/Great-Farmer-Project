from typing_extensions import Required
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Post, User, Product,Farmer,Customer,RATE_CHOICE
from django import forms
from django.core.validators import RegexValidator



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
    class Meta:
        rating=forms.ChoiceField(choices=RATE_CHOICE, widget=forms.Select(),required=True)
        model =Farmer
        fields = ('rating','user')
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields =['title','description','price', 'product','farmer']
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        self.fields['description'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        self.fields['price'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})
        self.fields['product'].widget.attrs.update({'type':'text', 'class':'form-control', 'id':'recipient-name'})
        self.fields['farmer'].widget.attrs.update({'type':'number', 'class':'form-control', 'id':'recipient-name'})

class MapForm(ModelForm):
    latitude=forms.DecimalField(required=True)
    longitude=forms.DecimalField(required=True)
    
    class Meta(UserCreationForm):
        model=User
        fields=['latitude','longitude']