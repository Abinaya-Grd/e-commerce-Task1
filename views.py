from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ================= HOME / PRODUCT LIST =================
@login_required(login_url='login')  # redirect to login page if not logged in
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# ================= PRODUCT DETAIL =================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

# ================= ADD TO CART =================
def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    id = str(id)
    cart[id] = cart.get(id, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

# ================= CART PAGE =================
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    if cart:
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            qty = cart[str(product.id)]
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})

    return render(request, 'store/cart.html', {'items': items, 'total': total})

# ================= CHECKOUT =================
@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = 0
    products = Product.objects.filter(id__in=cart.keys())

    for product in products:
        total += product.price * cart[str(product.id)]

    order = Order.objects.create(user=request.user, total_price=total)

    for product in products:
        OrderItem.objects.create(order=order, product=product, quantity=cart[str(product.id)])

    request.session['cart'] = {}  # clear cart after checkout
    return render(request, 'store/checkout.html', {'order': order})

# ================= MY ORDERS =================
@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

# ================= ORDER DETAIL =================
@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'store/order_detail.html', {'order': order, 'items': items})

# ================= LOGIN =================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')  # redirect to product list after login
        messages.error(request, "Invalid username or password")
    return render(request, 'store/login.html')

# ================= REGISTER =================
def register(request):
    if request.user.is_authenticated:
        return redirect('product_list')  # already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'store/register.html')

# ================= LOGOUT =================
def user_logout(request):
    logout(request)
    request.session['cart'] = {}  # clear cart on logout
    return redirect('login')
