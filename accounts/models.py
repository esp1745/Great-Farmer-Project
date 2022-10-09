from tkinter import CASCADE
from turtle import title
from urllib import request
from django.db import models
from django.db import connections
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from os import name






class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number= models.CharField(max_length=10)
    latitude=models.DecimalField(max_digits=22, decimal_places=16, null=True)
    longitude=models.DecimalField(max_digits=22, decimal_places=16, null=True)
    
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=True,primary_key=True)
    customer_type = models.CharField(max_length=10)
   

RATE_CHOICE=[
    (1,'1-trash'),
    (2,'2-bad'),
    (3,'3-ok'),
    (4,'4-good'),
    (5,'5-very good')
]
    
    
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=True,primary_key=True)
    rating= models.IntegerField(choices=RATE_CHOICE, blank=True, null=True)
     
     
    def __str__(self):
            return self.user.username

    
class Connection(models.Model):
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    farmer=models.ForeignKey(Farmer,on_delete=models.CASCADE, default=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, default=True)
    
    
    

class Product(models.Model):   
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date= models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=True)
    
   
   
    class meta:
           db_table="accounts_Product"

    def __str__(self):
             return self.product_name

class Post(models.Model):
    title=models.CharField(max_length=100, null=False)
    description=models.CharField(max_length=200,null=False)
    price=models.DecimalField(decimal_places=2, max_digits=10, null=False)
    farmer=models.ForeignKey(Farmer,on_delete=models.CASCADE, default=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, default=True)
    