from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
import json
import datetime
from .models import *

# Create your views here.


def home(request):
    return render(request, "home.html")


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist!!!')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken!!!')
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save();
                print('user created')
                
                return redirect('login')

        else:
            messages.info(request, 'password not matching!!!')
            return redirect('register')
       
    else:
        return render(request, "register.html")


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, 'Invalid credentials!!')
            return redirect('login')
    else:
        return render(request, "login.html")



def logout(request):
    auth.logout(request)
    return redirect('home')


def store(request):
     if request.user.is_authenticated:
         user = request.user
         order, created = Order.objects.get_or_create(user=user, complete=False)
         items = order.orderitem_set.all()
         print(items)
         cartItems = order.get_cart_items

     else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False} 
        cartItems = order['get_cart_items'] 

     arts = Art.objects.all()
     context = {'arts':arts, 'cartItems':cartItems}
     return render(request, 'store.html', context)

def cart(request):
     if request.user.is_authenticated:
         user = request.user
         order, created = Order.objects.get_or_create(user=user, complete=False)
         items = order.orderitem_set.all() 
         cartItems = order.get_cart_items
        
     else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items'] 
        
     context = {'items': items, 'order':order, 'cartItems':cartItems}
     return render(request, 'cart.html', context)

def checkout(request):
      if request.user.is_authenticated:
         user = request.user
         order, created = Order.objects.get_or_create(user=user, complete=False)
         items = order.orderitem_set.all()
         cartItems = order.get_cart_items
   
      else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False} 
        cartItems = order['get_cart_items'] 

      context = {'items': items, 'order':order, 'cartItems':cartItems}
      return render(request, 'checkout.html', context)

def updateItem(request):
      data = json.loads(request.body)
      artId = data['artId']
      action = data['action']

      print('Action:',action)
      print('artId:',artId)

      user = request.user
      art = Art.objects.get(id=artId)
      order, created = Order.objects.get_or_create(user=user, complete=False)
      orderItem, created = OrderItem.objects.get_or_create(order=order, art=art)

      if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
        
      elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

      orderItem.save()


      if orderItem.quantity <= 0:
          orderItem.delete()

      return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()        
    data = json.loads(request.body) 

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                user=user,
                order=order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )

    else:
        print('user not logged in..')

    return JsonResponse('Payment complete!!', safe=False)

def success(request):
       return render(request, "success.html")

def neworder(request):
     if request.method == "POST":
        art = NewOrder()
        art.name = request.POST.get('name')
        art.address = request.POST.get('address')
        art.type = request.POST.get('type')
        art.size = request.POST.get('size')
        art.phone_num = request.POST.get('phone_num')
        art.image = request.POST.get('image')

        if len(request.FILES) != 0:
            art.image = request.FILES['image']

        art.save()
        messages.success(request, "Product Added Successfully")
        return redirect('home')
     else:
        return render(request, "neworder.html")




#-----------------------------------------------------------------------------------------------------------------------------------------------------





def trying(request):
      return render(request, 'try.html')


