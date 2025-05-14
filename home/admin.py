from django.contrib import admin

# Register your models here.
admin.site.site_header = "Pizza Admin"
admin.site.site_title = "Pizza Admin Portal"    
admin.site.index_title = "Welcome to Pizza Admin Portal"

from .models import Pizza, Order
admin.site.register(Pizza)
admin.site.register(Order)