from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# =====================
# 🏷️ Category
# =====================
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# =====================
# 🛍️ Product
# =====================
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0


# =====================
# 🛒 CartItem
# =====================
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.user.username})"


# =====================
# ❤️ Wishlist
# =====================
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"


# =====================
# 📦 Order Grouping
# =====================
class OrderGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# =====================
# 🧾 Order Items
# =====================
class OrderItem(models.Model):
    order = models.ForeignKey(OrderGroup, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"


# =====================
# ⭐ Product Reviews
# =====================
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} → {self.rating}⭐"


# =====================
# 👤 Customer (Legacy - Optional)
# =====================
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =====================
# 🧾 (Optional) Legacy Single Order
# =====================
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.product.name} by {self.customer.first_name}"
