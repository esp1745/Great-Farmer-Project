from email.policy import default
from random import choices
from secrets import choice
from tkinter import CASCADE
from turtle import title
from urllib import request
from django.db import models
from django.db import connections
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from os import name

from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number= models.CharField(max_length=10)

class Customer(models.Model):
    latitude =models.CharField(max_length=100, null=True)
    longitude =models.CharField(max_length=100, null=True)
    customer_price=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    customer_rating = models.IntegerField(default=0, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classificatoin= models.CharField(max_length=10,default=0)
     
class Farmer(models.Model):
    rate = models.IntegerField(default=0, null=True)
    latitude =models.CharField(max_length=100, null=True)
    longitude =models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cluster =models.CharField(max_length=10, null=True)
    def __str__(self):
            return self.user.username

class Connection(models.Model):
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    farmer=models.ForeignKey(Farmer,on_delete=models.CASCADE, default=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, default=True)

class Product(models.Model):   
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    farmer = models.ManyToManyField(Farmer, null=True)
    
    class meta:
           db_table="accounts_Product"

    def __str__(self):
             return self.product_name

class Post(models.Model):
    title=models.CharField(max_length=100, null=False)
    description=models.CharField(max_length=200,null=False)
    price=models.DecimalField(decimal_places=2, max_digits=10, null=False)
    product=models.CharField(max_length=200, null=True)
    farmer=models.ForeignKey(Farmer,on_delete=models.CASCADE, default=True)
    
    

