from django.urls import path
from .import views
# from google import views as view


urlpatterns = [
    path('register/', views.register, name='register'),
    path('base/', views.base, name='base'),
    path('farmer_register/', views.farmer_register, name='farmer_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('home/', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('update/<int:id>/', views.updatepage, name='updatepage'),
    path('products/delete/<product_id>', views.deleteProduct, name = 'delete_product'),
    path('delete/<int:id>', views.deletepage),
    path('farmer/<int:id>/', views.farmer, name='farmer'),
    path('farmer/add_connection/<int:id>/', views.connect, name='connect'),
    path('connection/', views.connectionpage, name='connection'),
    path('post/', views.post, name='post'),
    path('farmerpost/', views.postpage, name='postpage'),
    path('updatepost/<int:id>/', views.updatepost, name='updatepost'),
    path('deletePost/<int:post_id>/', views.deletePost, name='deletepost'),
    path('map/customer/', views.maps_viewcustomer, name="maps_customer"),
    path('map/farmer/', views.maps_viewfarmer, name="maps_farmer"),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('cluster/', views.cluster, name="cluster"),
    path('all_farmers/', views.all_farmers, name='all_farmers'),
    
]  
