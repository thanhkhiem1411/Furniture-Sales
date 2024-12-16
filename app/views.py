from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse 
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)



# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        # messages.success(request, 'Đã thêm vào giỏ hàng')
        cartItems = order.get_cart_items
    else:
        items = []
        order  = {'get_cart_items': 0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order': order}
    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'app/home.html',context)

def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        # messages.success(request, 'Đã thêm vào giỏ hàng')
    else:
        items = []
        order  = {'get_cart_items': 0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order': order}
    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request,"app/product.html",context)

def article(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    return render(request,"app/article.html",context)
    
def cart(request):
    # Kiểm tra
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order  = {'get_cart_items': 0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request,"app/cart.html",context)

def checkout(request):
    # Kiểm tra
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order  = {'get_cart_items': 0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order': order,'cartItems': cartItems}
    return render(request,"app/checkout.html",context)



def updateItem(request):
    data = json.loads(request.body)
    # Lấy từ data
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    
    # User order gì thì lấy lại
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    # Thêm hành động
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    
    return JsonResponse('added', safe = False)

def detail(request):
    context = {}
    return render(request,"app/detail.html",context)

# Định nghĩa thêm hàm đăng ký và đăng nhập
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Mật khẩu không khớp. Vui lòng thử lại.")
            return redirect('register')

        # Tạo tài khoản người dùng mới
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        customer = Customer.objects.create(user=user, name=user.username, email=user.email)
        user.save()
        customer.save()
        
        messages.success(request, 'Bạn đã đăng ký thành công! Hãy đăng nhập để tiếp tục.')
        return render(request, "app/login.html")
    return render(request, "app/register.html")


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is not correct!!!')
    return render(request, "app/login.html")


# Search
def searchpage(request):
    context = {}
    if request.method == "POST":
        searched = request.POST['searched']
        product = Product.objects.filter(Q(name__contains=searched) | Q(code__contains=searched))
        
        return render(request, "app/searchpage.html", {'searched': searched, 'product': product})
    else:
        return render(request, "app/searchpage.html", context)

# Pay
def payPage (request):
    context ={}
    return render (request, "app/paypage.html", context)
    
# Profile
@login_required
def profileUser(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        # Cập nhật thông tin khách hàng
        if phone_number:
            customer.phone_number = phone_number
        if address:
            customer.address = address
        customer.save()

        return JsonResponse({'status': 'success'})

    else:
        context = {
            'user': user,
            'phone_number': customer.phone_number,
            'address': customer.address,
        }
        return render(request, 'app/profile.html', context)

def custom_logout(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return redirect('home')

    
    