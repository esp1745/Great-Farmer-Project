from itertools import product
from multiprocessing import context
from typing_extensions import Self
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import  CreateView
from .models import Connection, Post, User 
from .form import FarmerSignUpForm, CustomerSignUpForm, MapForm, productsForm,RateForm,PostForm,MapForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Product,Customer,Farmer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.conf import settings

import pandas as pd
import numpy as np
# from kmodes.kmodes import KModes
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pymysql
from sqlalchemy import create_engine
import requests
import googlemaps
import json
from django.conf import settings



def register(request):
    return render(request, '../templates/register.html')



# @unauthenticated_user
# @allowed_users(allowed_roles=['farmer'])

def farmer_register(request):
    form = FarmerSignUpForm()   
    # if request.method =='POST':
    #     far = request.POST.get('farmer')
    #     cus = request.POST.get('customer')
    #     user = None
    #     if far:
    #         user = user.objects.get(user=user, is_farmer=True)
    #     elif cus:
    #         user = user.objects.get(user=user, is_customer=True)
    #     # user=form.save()
    form= FarmerSignUpForm(request.POST)
        
    if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            user = form.save()
            user.is_farmer = True
            # Farmer.objects.create(user=user, user_id=form.cleaned_data.get('user_id'))
            username = form.cleaned_data.get('username')
            group= Group.objects.get(name='Farmer')
            
            user.groups.add(group)
            messages.success(request,'Account created' ''+ username)
            return redirect('loginpage')
    context={'form':form}
    return render(request, '../templates/farmer_register.html', context)
    
        
        
# @unauthenticated_user
# @allowed_users(allowed_roles=['customer'])
def customer_register(request):
   
     form = CustomerSignUpForm()
         
     if request.method =='POST':
         form= CustomerSignUpForm(request.POST)
         if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            user = form.save()
            user.is_customer = True
            #  Customer.objects.create(user=user,phone_number=form.cleaned_data.get('type'))
            
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            
            user.groups.add(group)
            messages.success(request,'Account created' ''+ username)
            return redirect('loginpage')
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
    context={'list':list,'post':post,'pos':pos}
    return render(request, 'home.html', context )
    

    

def logoutUser(request):
    logout(request)
    return redirect('loginpage')

def geocode(request):

    URL = "https://maps.googleapis.com/maps/api/geocode/json"
  
    location = "university of zambia"
    
    GOOGLE_API_KEY='AIzaSyChfcK6kfbgrOH9B5zXEokJGKz4FO8qC2g'
  
    PARAMS = {'address':location, 'key':GOOGLE_API_KEY}
    r = requests.get(url = URL, params = PARAMS)

    data = r.json()

  
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    formatted_address = data['results'][0]['formatted_address']

    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"%(latitude, longitude,formatted_address))
   
    return render(request,'geocode.html')

def farmer(request):
    form=RateForm()
    # user=User.objects.get()
    user=request.user
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit = False)
            rate.user =request.user
            rate.save()
    context={'form':form, 'user':user}       
    return render(request,'farmer.html',context)
 

## adding a product

# @allowed_users(allowed_roles=['Farmer'])
def product(request):
    list = Product.objects.all()
    form = productsForm()
    if request.method == 'POST':
        form = productsForm(request.POST)
    
    if form.is_valid():
        
        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()
        
        return redirect('product')     
    context = {'form':form, 'list':list}
    return render(request, 'product.html',context)



@allowed_users(allowed_roles=['Farmer'])
def updatepage(request, id):
    list = Product.objects.get(id=id)
    pos = Post.objects.get(id=id)
    form = productsForm(request.POST, instance= list)
    if form.is_valid():
        form.save()
        return redirect('home')
    context={'list':list,'pos':pos}
    return render(request, "update.html", context,)
  

 
@allowed_users(allowed_roles=['Farmer'])
def deletepage(request, id):
    list = Product.objects.get(id=id)
    pos= Post.objects.get(id=id)
    list.delete()
    
    context= {'list':list,'pos':pos}
    return render(request, 'delete.html',context)
   
def post(request):
    pos = Post.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
    
    if form.is_valid():
        
        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()
        
        return redirect('post')     
    context = {'form':form, 'pos':pos}
    return render(request, 'post.html',context)

def maps_view(request):
    
    form=MapForm()
    if request.method=='POST':
        form=MapForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('map') 
       
    return render(request,'map.html', {'google_api_key': settings.GOOGLE_API_KEY})

# # data= pd.read_sql[   
# #         'default': {
# #         'ENGINE': 'django.db.backends.mysql',
# #         'NAME': 'farm_db',
# #         'USER': 'root',
# #         'PASSWORD': '',
# #         'PORT': 3306,
# #         'HOST': '127.0.0.1',
# #     }]
# db_connection='mysql+pymysql://root@127.0.0.1:3306/farm_db'
# conn=create_engine(db_connection)
# df=pd.read_sql("select user_id,price from accounts_product",conn)
# print(data.columns)

# newD = data[['farmer_id', ' products']]
# print(newD)
# newD= newD.set_index('farmer_id')

# inertias = []

# for i in range(1,11):
#     kmeans = KMeans(n_clusters=i)
#     kmeans.fit(df)
#     inertias.append(kmeans.inertia_)

# plt.plot(range(1,11), inertias, marker='o')
# plt.title('Elbow method')
# plt.xlabel('Number of clusters')
# plt.ylabel('Inertia')
# plt.show()

# kmeans = KMeans(n_clusters=2)
# kmeans.fit(df)

# plt.scatter(x, y, c=kmeans.labels_)
# plt.show()

# cost = []
# K = range(1,9)
# for num_clusters in list(K):
#      kmode = KModes(n_clusters=num_clusters, init = "random", n_init = 20, verbose=1)
#      kmode.fit_predict(D_T_FMT)
#      cost.append(kmode.cost_)
    
# plt.plot(K, cost, 'bx-')
# plt.xlabel('No. of clusters')
# plt.ylabel('Cost')
# plt.title('Elbow Method For Optimal k')
# plt.show()

# kmode = KModes(n_clusters=9, init = "random", n_init = 20, verbose=1)
# clusters = kmode.fit_predict(df)
# print(clusters)

# df.insert(0, "Cluster", clusters, True)
# print (df)