from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Static Pages
    path("", views.home, name='home'),
    path("about/", views.about, name="about"),
    

    # 🔹 Authentication
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name='register'),

    # 🔹 Product Pages
    path("product/<int:pk>/", views.product, name='product'),
    path("categories/", views.categories, name='categories'),
    path("categories/<int:category_id>/", views.categories, name='category_products'),

    # 🔹 Cart Operations
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name='add_to_cart'),
    path("cart/", views.cart_view, name='cart'),
    path("checkout/", views.checkout_view, name='checkout'),
    path("cart/update/<int:item_id>/", views.update_cart_quantity, name="update_cart"),

    # 🔹 Wishlist Operations
    path("wishlist/", views.wishlist_view, name='wishlist_view'),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name='add_to_wishlist'),
    path("wishlist/remove/<int:product_id>/", views.remove_from_wishlist, name='remove_from_wishlist'),

    # 🔹 Reviews
    path("product/<int:product_id>/review/", views.submit_review, name='submit_review'),

    # 🔹 Search
    path("search/", views.search_results, name='search_results'),
]
