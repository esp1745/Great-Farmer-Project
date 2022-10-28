from itertools import product
from multiprocessing import context
from typing_extensions import Self
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import  CreateView
from .models import Connection, Post, User
from .form import FarmerSignUpForm, CustomerSignUpForm, MapFormCustomer, MapFormFarmer,productsForm,PostForm, RateForm,UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Product,Customer,Farmer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.conf import settings
from django.http import JsonResponse
from django.db.models import QuerySet as Q
# from .task import myTask

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sklearn.cluster as cluster
import pymysql
from sqlalchemy import create_engine
import seaborn as sns
import requests
import googlemaps
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import threading
from django.conf import settings
from sklearn.preprocessing import MinMaxScaler, StandardScaler



def register(request):
    return render(request, '../templates/register.html')

def base(request):
    return render(request, '../templates/base.html')
# @unauthenticated_user
# @allowed_users(allowed_roles=['farmer'])

def farmer_register(request):
    form = FarmerSignUpForm()   
    if request.method == 'POST':
        form= FarmerSignUpForm(request.POST)
        
        
        if form.is_valid():
            usernam = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1') 
            
            instance=form.save(commit=False)
            instance.user = request.user
            instance.save()
            user = form.save()
            
            new_user = authenticate(username=usernam, password=password)
            if new_user is not None:
                login(request, new_user)
            
            user.is_farmer = True
            Farmer.objects.create(user=user)
            username = form.cleaned_data.get('username')
            group= Group.objects.get(name='Farmer')
            
            user.groups.add(group)
            messages.success(request,'Account created' ''+ username)
            return redirect('maps_farmer')
    context={'form':form}
    return render(request, '../templates/farmer_register.html', context)
           
# @unauthenticated_user
# @allowed_users(allowed_roles=['customer'])
def customer_register(request):
   
     form = CustomerSignUpForm()
         
     if request.method =='POST':
         form= CustomerSignUpForm(request.POST)
         if form.is_valid():
            usernam = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1') 
            
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            user = form.save()
            
            new_user = authenticate(username=usernam, password=password)
            if new_user is not None:
                login(request, new_user)
            
            user.is_customer = True
            
            
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            
            user.groups.add(group)
            messages.success(request,'Account created' ''+ username)
            return redirect('maps_customer')
     context={'form':form}
     return render(request, '../templates/customer_register.html', context)

# @allowed_users(allowed_roles=['farmer', 'customer'])
def loginpage(request):
    
    if request.method =='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        
        user=authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_farmer:
                return redirect('home') 
            elif user.is_authenticated and user.is_customer:
                return redirect('home')
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
        
    context={}
    return render(request, '../templates/login.html', context)

def home(request):
    list = Product.objects.all()
    pos=Post.objects.all() 
    post=Connection.objects.all()
    farm=Farmer.objects.all()
    context={'list':list,'post':post,'pos':pos,'farm':farm}
    return render(request, 'home.html', context )
    
def logoutUser(request):
    logout(request)
    return redirect('loginpage')


def farmer(request,id):
    form=RateForm()
    farmer = Farmer.objects.get(pk=id)
    if request.method == 'POST':
        form = RateForm(request.POST or None, instance = farmer)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.rate = farmer.rate
            # instance = farmer.user
            instance.save()
            return redirect('home')
    return render(request, 'farmer.html', {'farmer':farmer, 'form':form})
      
## adding a product
# @allowed_users(allowed_roles=['Farmer'])
def product(request):
    list = Product.objects.all()
    form = productsForm()
    if request.method == 'POST':
        form = productsForm(request.POST)
    
    if form.is_valid():
        current_user = request.user
        farmer = Farmer.objects.get(user = current_user)
        instance=form.save(commit=False)
        instance.save()
        instance.farmer.add(farmer)
        cluster(request)
        return redirect('product')     
    context = {'form':form, 'list':list}
    return render(request, 'product.html',context)

@allowed_users(allowed_roles=['Farmer'])
def updatepage(request, id):
    list = Product.objects.get(pk=id)
    form = productsForm(request.POST or None, instance= list)
    if form.is_valid():
        form.save()
        return redirect('product')
    context={'list':list,'form':form}
    return render(request, "update.html", context)
@allowed_users(allowed_roles=['Farmer'])  
def deleteProduct(request, product_id):
    list = Product.objects.get(pk=product_id)
    list.delete()
    return redirect('product')

@allowed_users(allowed_roles=['Farmer'])
def deletepage(request, id):
    list = Product.objects.get(id=id)
    pos= Post.objects.get(id=id)
    list.delete()
    
    context= {'list':list,'pos':pos}
    return render(request, 'delete.html',context)
#post section
def post(request):
    pos = Post.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
    
    if form.is_valid():
        
        instance=form.save(commit=False)
        instance.farmer=request.user
        instance.save()
        
        return redirect('post')     
    context = {'form':form, 'pos':pos}
    return render(request, 'post.html',context)

@allowed_users(allowed_roles=['Farmer'])
def updatepost(request, id):
    pos = Post.objects.get(pk=id)
    form = PostForm(request.POST or None, instance= pos)
    if form.is_valid():
        form.save()
        return redirect('post')
    context={'pos':pos,'form':form}
    return render(request, "updatepost.html", context)

def deletePost(request, post_id):
    pos = Post.objects.get(pk=post_id)
    pos.delete()
    return redirect('post')

def maps_viewfarmer(request):
    user = request.user
    farmer = Farmer.objects.get(user = user)
    form=MapFormFarmer()
    if request.method=='POST':
        form=MapFormFarmer(request.POST, instance=farmer)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.latitude = request.POST.get('latitude')
        instance.longitude = request.POST.get('longitude')
        instance.save()
        return redirect('home') 
       
    return render(request,'mapfarmer.html', {'google_api_key': settings.GOOGLE_MAPS_API_KEY})

def maps_viewcustomer(request):
    
    form=MapFormCustomer()
    if request.method=='POST':
        form=MapFormCustomer(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.latitude = request.POST.get('latitude')
        instance.longitude = request.POST.get('longitude')
        instance.save()
        return redirect('home') 
    return render(request,'mapcustomer.html', {'google_api_key': settings.GOOGLE_MAPS_API_KEY})

def connect(request,id):
    farmer=Farmer.objects.get(pk=id)
    Connection.objects.create(farmer=farmer, customer=request.user)
    return redirect('home')

def connectionpage(request):
    conn= Connection.objects.all()
    return render(request, 'connection.html',{'conn':conn})
def postpage(request):
    entries=Post.objects.all()
    return render(request, 'farmerpost.html',{'entries':entries})

def profile(request,id):
    id=request.user.id
    user=User.objects.get(pk=id)
    form=UserProfile(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request,'profile.html',{'form':form})
    


def cluster(request):
    sqlEngine= create_engine('mysql+pymysql://root:@127.0.0.1:3306/farm_db', pool_recycle=3600)
    dbConnection= sqlEngine.connect()
    frame  = pd.read_sql("select accounts_product.price,accounts_farmer.latitude, accounts_farmer.longitude FROM accounts_product JOIN accounts_product_farmer ON accounts_product.id=accounts_product_farmer.product_id JOIN accounts_farmer ON accounts_farmer.id=accounts_product_farmer.farmer_id", dbConnection);
    pd.set_option('display.expand_frame_repr', False)
    
    X= frame.iloc[:, [0,1,2]].values
    y=range(1,9)
    wcss=[]
    for i in y:
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=0)
        kmeans=KMeans(n_clusters=3)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
        
    
    kmeansmodel = KMeans(n_clusters= 3, init='k-means++', random_state=0)
    y_kmeans= kmeansmodel.fit_predict(X)
   
   
    frame.insert(0,'cluster',y_kmeans,True)
    
    farmers = Farmer.objects.all()
    m = len(farmers)
    for i in range(m):
        farmers[i].c = y_kmeans[i]
        farmers[i].save()
        # farmers = Farmer.objects.bulk_update(objs=farmers, fields=['c'], batch_size=m)
        
    # pr = Product.farmer
    print(frame)
    return redirect('home')

