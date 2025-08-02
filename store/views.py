from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q, Value
from django.db.models.functions import Replace, Lower
from datetime import datetime

from .forms import SignupForm
from .models import Category, Product, CartItem, OrderGroup, OrderItem, Wishlist, Review

# 🔹 Home Page
def home(request):
    request.session['last_visit'] = str(datetime.now())
    request.session['visit_count'] = request.session.get('visit_count', 0) + 1
    products = Product.objects.all()

    cart_products = []
    wishlist_products = []
    if request.user.is_authenticated:
        cart_products = CartItem.objects.filter(user=request.user).values_list('product_id', flat=True)
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, "store/home.html", {
        'Products': products,
        'cart_products': cart_products,
        'wishlist_products': wishlist_products
    })

# 🔹 About Page
def about(request):
    last_visit = request.session.get('last_visit', 'Never visited before!')
    visit_count = request.session.get('visit_count', 0)
    return render(request, "store/about.html", {
        'last_visit': last_visit,
        'visit_count': visit_count
    })

# 🔹 Product Detail Page
def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    is_in_cart = is_in_wishlist = False
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    if request.user.is_authenticated:
        is_in_cart = CartItem.objects.filter(user=request.user, product=product).exists()
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, "store/product.html", {
        'product': product,
        'is_in_cart': is_in_cart,
        'is_in_wishlist': is_in_wishlist,
        'reviews': reviews,
        'average_rating': product.average_rating

    })

# ⭐ Submit Product Review
@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={"rating": rating, "comment": comment}
        )
        messages.success(request, "Thank you! Your review has been submitted.")
        return redirect('product', pk=product.id)
    return redirect('home')

# 🔹 Login
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You have been logged in")
                return redirect('home')
            messages.error(request, "Invalid username or password")
        return render(request, "store/login.html")
    return redirect("home")

# 🔹 Logout
def logout_user(request):
    logout(request)
    request.session.pop('last_visit', None)
    request.session.pop('visit_count', None)
    messages.success(request, "You have been logged out.")
    return redirect("home")

# 🔹 Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'store/register.html')

# 🔹 Categories
def categories(request, category_id=None):
    all_categories = Category.objects.all()
    current_category = None
    products = []

    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=current_category)

    wishlist_products = []
    cart_products = []
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        cart_products = CartItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, "store/categories.html", {
        'all_categories': all_categories,
        'current_category': current_category,
        'products': products,
        'wishlist_products': wishlist_products,
        'cart_products': cart_products
    })

# 🔹 Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

# 🔹 Cart View
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

# 🔹 Checkout
@login_required
def checkout_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)

    if not items.exists():
        messages.warning(request, "Your cart is empty. Add items before checkout.")
        return redirect('cart')

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment_mode = request.POST.get("payment_mode")

        order_group = OrderGroup.objects.create(
            user=request.user,
            total_price=total,
            is_paid=True if payment_mode.lower() == 'online' else False,
            shipping_address=address,
            phone=phone
        )

        for item in items:
            OrderItem.objects.create(
                order=order_group,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        items.delete()

        send_mail(
            subject='🛒 Order Confirmation',
            message=f"Hi {name}, your order has been placed successfully!",
            from_email=None,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        messages.success(request, f"Order placed! Confirmation sent to {request.user.email}")
        return redirect('home')

    return render(request, 'store/checkout.html', {'items': items, 'total': total})

# 🔹 Update Cart Quantity
@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return redirect('cart')
        cart_item.save()
    return redirect('cart')

# ⭐ Wishlist Functionality
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"{product.name} added to your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, "Item removed from wishlist.")
    return redirect('wishlist_view')

# 🔍 Search
def search_results(request):
    query = request.GET.get('q', '').strip()

    if query:
        normalized_query = query.replace(" ", "").lower()
        results = Product.objects.annotate(
            norm_name=Lower(Replace('name', Value(' '), Value(''))),
            norm_desc=Lower(Replace('description', Value(' '), Value('')))
        ).filter(
            Q(norm_name__icontains=normalized_query) |
            Q(norm_desc__icontains=normalized_query)
        )
    else:
        results = []

    wishlist_products = []
    cart_products = []
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        cart_products = CartItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'store/search_results.html', {
        'query': query,
        'results': results,
        'wishlist_products': wishlist_products,
        'cart_products': cart_products
    })
