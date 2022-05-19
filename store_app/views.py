from audioop import reverse
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *


# Index view
def index_view(request):

    # Retrieve 5 testimonials from database
    testimonials = Testimonial.objects.all()[:5]

    # If user is authenticated take them to a authenticated main page
    if request.user.is_authenticated:
        # Render main page for authenticated request user
        return render(request, "store_app/index.html", {
            "user": request.user,
            "testimonials": testimonials
        })

    # Otherwise take the user to a non-authenticated main page
    return render(request, "store_app/index.html", {
        "testimonials": testimonials
    })


def login_view(request):

    # If request method is POST try and authenticate request user
    if request.method == "POST":
        # Assign form data
        username = request.POST['username']
        password = request.POST['password']

        if (not username) or (not password):
            return render(request, "store_app/login.html", {
                "message": "Please fill out the form completely"
            })

        # Try and authenticate user with form data
        try:
            user = User.objects.get(username=username, password=password)

            # If user exists login and redirect to the main page
            if user:
                login(request, user)
                return redirect("index")

        # If user object does not exist render login page with corresponding message
        except User.DoesNotExist:
            return render(request, "store_app/login.html", {
                "message": "Account for this user does not exist"
            })

    # Otherwise return the login page
    return render(request, "store_app/login.html")


@login_required
def logout_view(request):

    # Log out user and redirect them to the main page
    logout(request)
    return redirect("index")


def register_view(request):

    # If request method is POST proceed with register functionality
    if request.method == "POST":

        # get username, email, password, and password confirmation from user (form data)
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm']
        left_handed = request.POST['left-handed']

        if (not username) or (not email) or (not address) or (not password) or (not confirm_password):
            return render(request, "store_app/register.html", {
                "message": "Please fill out the form completely"
            })

        # If password and confirmation don't match return the register page with error message
        if password != confirm_password:
            return render(request, "store_app/register.html", {
                "message": "Passwords must match"
            })
        
        if left_handed == "true":
            lefty = True
        else:
            lefty = False


        user, created = User.objects.get_or_create(username=username, email=email, password=password, address=address, is_left_handed=lefty)

        if created:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "store_app/register.html", {
                "message": "User with this information already exists"
            })

    # Otherwise return the register page
    return render(request, "store_app/register.html")


def search_view(request):

    # Prompt user from a search query
    query = request.GET['query']

    # Get all matching results from the database where product names include user query case-insensitively
    search_results = Product.objects.all().filter(name__icontains=query)

    # Pagination
    paginator = Paginator(search_results, 16)

    # Get page number from user and pass corresponding results object to context
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    # Return search results to user
    return render(request, "store_app/search.html", {
        "query": query,
        "results": page_object
    })


def about_view(request):
    # Render About page
    return render(request, "store_app/about.html")


def products_view(request):

    # Get a list of products from the database
    products_list = Product.objects.all()

    # Pagination
    paginator = Paginator(products_list, 16)

    # Get page number from user and pass corresponding products object to context
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    # Render the products page with the corresponding page
    return render(request, "store_app/products.html", {
        "products": page_object
    })


def product_view(request, id):
    
    # Get Item from database
    product = Product.objects.get(id=id)

    message = request.session.get("cart-message", "")

    request.session["cart-message"] = ""

    # Render product item page
    return render(request, "store_app/product.html", {
        "product": product,
        "message": message
    })


@login_required
def account_view(request):

    # Pass user's purchase history to context
    user_purchases = Purchase.objects.filter(user=request.user)

    # Pass user's purchase amount to context
    amount = len(user_purchases)

    # Render user's account page
    return render(request, "store_app/dashboard.html", {
        "user": request.user,
        "purchases": user_purchases,
        "amount": amount
    })


@login_required
def add_to_cart(request, id):

    if request.method == "POST":

        # Obtain data from user
        quantity = request.POST["quantity"]

        # Get product object from database
        product = Product.objects.get(id=id)
    
        # If object exists in cart tell user it does and if it does not exist create object in cart
        _, created = Cart.objects.get_or_create(cart_user=request.user, cart_product=product, quantity=quantity)

        # Store message in session
        if created:
            request.session["cart-message"] = "Product was successfully added to cart"
        else:
            request.session["cart-message"] = "Product is already in cart"

    # Redirect user to product page
    return redirect("product", id=id)


@login_required
def cart_view(request):
    
    # Obtain user's cart from database and pass it to context
    user_cart = Cart.objects.filter(cart_user=request.user)

    # Render user's cart
    return render(request, "store_app/cart.html", {
        "cart": user_cart
    })


@login_required
def checkout_view(request):
    print("GET Checkout")

    # Implement basic test checkout without credentials
    if request.method == 'POST':
        print("POST works")
        # Obtain user's cart from database
        user_cart = Cart.objects.filter(cart_user=request.user)

        for item in user_cart:
            Purchase.objects.create(user=request.user, product=item.cart_product, quantity=item.quantity)
        
        user_cart.delete()
        
        return redirect("accounts")

    # Render checkout page for user
    return render(request, "store_app/checkout.html")


@login_required
def remove_view(request):

    if request.method == 'POST':

        product_id = request.POST["id"]

        # Remove product from user's cart
        product = Product.objects.get(id=product_id)
        Cart.objects.filter(cart_product=product).delete()
    
    # Redirect user to their cart
    return redirect("cart")


@login_required
def rating_view(request):
    
    if request.method == 'POST':

        # Obtain purchase id and purchase rating from user
        purchase_id = request.POST["purchase_id"]
        submitted_rating = request.POST["rating"]

        # Search for purchase in database and update it's rating
        purchase_object = Purchase.objects.get(id=purchase_id)
        purchase_object.rating = int(submitted_rating)
        purchase_object.save()
        return render(request, "store_app/dashboard.html", {
            "message": "Your rating was submitted"
        })

    # If route is requested with GET method return bad request
    # return HttpResponseBadRequest("The page you are trying to reach does not exist")
    return HttpResponse("Requested page does not exist")