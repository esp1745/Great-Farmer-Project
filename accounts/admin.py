from django.contrib import admin
from .models import User, Product, Farmer, Customer, Connection

# Register your models here.
admin.site.register(User)
admin.site.register(Farmer)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Connection)
