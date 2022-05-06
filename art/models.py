from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class NewOrder(models.Model):
    name = models.TextField(max_length=100)
    address = models.TextField(max_length=300, null=False)
    phone_num = PhoneNumberField(null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    type = models.CharField(max_length=30)
    size = models.TextField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    

class Art(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


#Order = cart; OrderItem = items in cart 
class Order(models.Model):                                                    #for nth order details
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)    #cnctng user table frm pgadmin
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)                              # if false = open cart ,we can buy in tis 'order'(1) ; true = closed cart, buy items in diff 'order'(2)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            shipping = True
        return shipping
         

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 


class OrderItem(models.Model):                                                 #for ordered items details
    art = models.ForeignKey(Art, on_delete=models.SET_NULL, null=True)         #connctng 'Art' table(for ordered 'art' details)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)      #cnnctng 'Order' table ( for single 'order' can have multiple 'orderitems's)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.art.price * self.quantity
        return total



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address