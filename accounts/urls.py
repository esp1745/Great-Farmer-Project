from django.urls import path
from .import views
# from google import views as view


urlpatterns = [
    path('register/', views.register, name='register'),
    path('farmer_register/', views.farmer_register, name='farmer_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('home/', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('update/<int:id>/', views.updatepage, name='updatepage'),    
    path('delete/<int:id>', views.deletepage),
    path('geocode/',views.geocode, name='geocode'),
    path('farmer/',views.farmer, name="farmer"),
    path('post/', views.post, name='post'),
    path('map/', views.maps_view, name="maps_view"),
    
]
