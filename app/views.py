from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse 
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ArticleForm, DeliveryForm
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)



# Create your views here.
def home(request):
    is_admin = request.session.get('admin', False)
    if request.user.is_authenticated and not is_admin:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer = customer, complete = False)
            items = order.orderitem_set.all()
            # messages.success(request, 'Đã thêm vào giỏ hàng')
            cartItems = order.get_cart_items
    else:
        items = []
        order  = {'get_cart_items': 0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
    articles = Article.objects.all()
    context = {'items':items, 'order': order, 'articles':articles}
    products = Product.objects.all()
    context.update({'products':products,'cartItems':cartItems})
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request, 'app/home.html',context)

#main 
def product(request):
    is_admin = request.session.get('admin', False)
    if request.user.is_authenticated and not is_admin:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {'items':items, 'order': order ,'cartItems':cartItems}
        # messages.success(request, 'Đã thêm vào giỏ hàng')
    else:
        items = []
        order  = {'get_cart_items': 0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
        context = {'items':items, 'order': order, 'cartItems':cartItems}
    products = Product.objects.all()
    context = {'products':products}
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request,"app/product.html",context)

def article(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request,"app/article.html",context)
    
#cart -> checkout
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
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request,"app/cart.html",context)

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
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request,"app/checkout.html",context)



# Pay
def payPage(request):
    submitted = False 
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer=customer, complete=False)
        form = DeliveryForm(initial={'customer': customer, 'order': order})
        
        if request.method == 'POST':
            form = DeliveryForm(request.POST)
            if form.is_valid():
                form.save()
                order.complete = True
                order.save()
                # Construct the message with order details
                order_items = order.orderitem_set.all()
                order_details = "\n".join([f"{item.product.name}: {item.quantity} x {item.product.price} VNĐ" for item in order_items])
                total_amount = order.get_cart_total

                message = f"""
                Hi {customer.name}, You have successfully placed an order at HomeClick!

                Order Details:
                {order_details}

                Total Amount: {total_amount} VNĐ

                We hope you enjoy our service!
                """

                sendMail("Xác nhận đặt hàng thành công", message, customer.email)
                return HttpResponseRedirect('/addProduct?submitted=True')
    else:
        form = DeliveryForm()
        if 'submitted' in request.GET:
            submitted = True
    
    context = {'form': form, 'submitted': submitted}
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request, "app/paypage.html", context)
    
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


    
def detail(request):
    context = {}
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request,"app/detail.html",context)

#Account
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
            if not hasattr(request.user, 'customer'):
                request.session['admin'] = True
            return redirect('home')
        else:
            messages.info(request, 'Username or password is not correct!!!')
    return render(request, "app/login.html")


def custom_logout(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return redirect('home')


# Admin role

# Article
def addArticle(request):
    submitted = False
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addArticle?sumitted=True')
    else:
        form = ArticleForm
        if 'submitted' in request.GET:
            submitted = True
    context = {'form_A': form, 'submitted': submitted}
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})
    return render(request, 'app/addArticle.html', context)

#Product
def addProduct(request):
    submitted = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addProduct?submitted=True')
    else:
        form = ProductForm  
        if 'submitted' in request.GET:
            submitted = True
    context = {'form': form, 'submitted': submitted}
    is_admin = request.session.get('admin', False)
    context.update({'is_admin': is_admin})

    return render(request, 'app/addproduct.html', context)

#util 

# Search
def searchpage(request):
    context = {}
    if request.method == "POST":
        searched = request.POST['searched']
        product = Product.objects.filter(Q(name__contains=searched) | Q(code__contains=searched))
        
        return render(request, "app/searchpage.html", {'searched': searched, 'product': product})
    else:
        return render(request, "app/searchpage.html", context)
    
def sendMail(subject, message, receiver):
    sender = settings.EMAIL_HOST_USER
    send_mail(
                subject,
                message,
                sender,
                [receiver],
                fail_silently=False,
            )