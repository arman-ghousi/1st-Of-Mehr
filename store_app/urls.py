from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.index_view, name="index"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('search', views.search_view, name="search"),
    path('about', views.about_view, name="about"),
    path('products', views.products_view, name="products"),
    path('product/<int:id>', views.product_view, name="product"),
    path('accounts', views.account_view, name="accounts"),
    path('cart', views.cart_view, name="cart"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add"),
    path('checkout', views.checkout_view, name="checkout"),
    path('remove', views.remove_view, name="remove"),
    path('rating', views.rating_view, name="rating")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
