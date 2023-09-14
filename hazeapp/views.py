from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


def index(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    newarrivals = ProductCollection.objects.get(name='New Arrivals')
    products = newarrivals.products.all()

    context = {'products': products,'cartItems': cartItems}
    return render(request, 'index.html', context)




def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    may = ProductCollection.objects.get(name='Hoodie Hunch')
    products = may.products.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store.html', context)

def product_details(request, name):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    product = get_object_or_404(Product, name=name)
    
   
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'product_detail.html', context)    


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)





def contact(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'account/contact.html', context)

def faq(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'account/faq.html', context)

def loginUser(request):


    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request, "Incorrect Email or Password")    
    
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}    
    
    return render(request, 'account/login.html', context)   

def register(request):

    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')
        #print(username, email)
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists! Login to continue") 
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists!") 
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()  
                    data = Customer.objects.create(user=user, first_name=first_name,last_name=last_name, email=email, phone=phone)
                    data.save()

                    # Login Code for user
                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        return redirect('home')
        else:
            messages.info(request, "Passwords doesn't match") 
            return redirect('register')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}


    return render(request, 'account/register.html', context)     
    

def logoutUser(request):
    logout(request)
    return redirect('home')  


def account(request):
    data = cartData(request)
    cartItems = data['cartItems']
    customer = request.user.customer

    orders = []
    order_items = OrderItem.objects.filter(order__customer=customer, order__complete=True).order_by('-date_added')

    for item in order_items:
        order = {
            'product_name': item.product.name,
            'date_ordered': item.order.date_ordered,
            'quantity': item.quantity
        }
        orders.append(order)

    shipping_address = ShippingAddress.objects.filter(customer=customer).last()

    context = {
        'cartItems': cartItems,
        'customer': customer,
        'orders': orders,
        'shipping_address': shipping_address
    }
    return render(request, 'account.html', context)
