from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create Users model

# Create Products model
class Product(models.Model):

    CATEGORIES = [
        ("pencils", "Pencils"),
        ("pens", "Pens"),
        ("notebooks", "Notebooks"),
        ("brushes", "Brushes"),
        ("calculators", "Calculators"),
        ("calendars", "Calendars"),
        ("gifting", "Gifting"),
        ("lamps", "Lamps"),
        ("coloring", "Coloring"),
        ("postcards", "Postcards"),
        ("postages", "Postages"),
        ("scissors", "Scissors")
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    price = models.FloatField(blank=False, null=False)
    category = models.CharField(max_length=50, choices=CATEGORIES)    
    creation_date = models.DateTimeField(auto_now_add=True)
    availability = models.IntegerField()
    image = models.ImageField(upload_to=settings.MEDIA_ROOT)
    is_left_hand_compatible = models.BooleanField(default=False)

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_left_handed = models.BooleanField(null=False, blank=False, default=False)
    address = models.TextField(null=False, blank=False)


class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchase_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_product")
    quantity = models.IntegerField()
    rating = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(auto_now_add=True)


class Testimonial(models.Model):
    id = models.AutoField(primary_key=True)
    testimonial = models.TextField(null=False, blank=False)


class Cart(models.Model):
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_user")
    cart_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_product")
    quantity = models.IntegerField(null=False, blank=False)
