from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer,complete=False)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0 , 'get_cart_items':0,'shipping':False}
        cartItems = cart['get_cart_items']

    products = Product.objects.all()
    context = {
        'products' : products,
        'cartItems' : cartItems
    }
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer,complete=False)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items


    else:
        items = []
        cart = {'get_cart_total':0 , 'get_cart_items':0,'shipping':False}
        cartItems = cart['get_cart_items']

    context = {
        'items' : items,
        'cart' : cart,
        'cartItems' : cartItems
    }
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer,complete=False)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0 , 'get_cart_items':0,'shipping':False}
        cartItems = cart['get_cart_items']
    context = {
        'items' : items,
        'cart' : cart,
        'cartItems' : cartItems
    }
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    print('product_id:',product_id)
    print('action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    cart,created = Cart.objects.get_or_create(customer=customer,complete=False)
    cartItem,created = CartItem.objects.get_or_create(cart=cart,product=product)

    if action == 'add':
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)

    cartItem.save()

    if cartItem.quantity <= 0:
        cartItem.delete()
    return JsonResponse('Item is added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)   
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        print(total)
        cart.transaction_id = transaction_id

        if total == 55:
            cart.complete = True
        cart.save()

        if cart.shipping == True:
            ShippingAddress.objects.create(
			customer=customer,
			cart=cart,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
    else:
        print('User is not logged in')
    return JsonResponse('Payment completed',safe=False)