from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Art)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(NewOrder)