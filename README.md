# 1st Of Mehr

1st of Mehr is an ecommerce project made with Django and the theme of the project is about office supplies.
It does not hold checkout as it is for demonstrational Purposes .. .

## How to use

clone or download the project inside a directory on your system and run ` python manage.py runserver ` for it to run on your localhost (Ususally on port 8000)

## What will you find in each file

### first_of_mehr/

This is the main Django project directory which holds the basic settings of the project

### store_app/

This directory consists of the necessary files for the project. the contents of this directory are as follows:

#### static/

This folder holds all the static assets for the project where each route loads its corresponding asset.

#### templates/

This folder holds all the HTML template files of the project.

#### templatetags/

In this folder there is a python file to be used as a custom jinja tag for multiplying numbers inside the templates

#### admin.py

In this python file all models are registered to the admin site for better manipulation of data.

#### models.py

In this file there are multiple models such as Product to store product information inside the database; A basic User model to handle user data and authentication within the application. Purchase model which defines user's purchase each time they make one. Testimonial which will mainly hold user testimonials to be displayed later on the main page, and lastly the Cart model to store user's cart before finalizing purchase.

#### urls.py

This python file has all the routes for the application, each of which are for a specific page .

#### views.py

This file control all user interactions with the application such as user authentication, product search, products page and pagination, rendering each product's page and user's dashboard. This file also handles adding to cart and removing from it, rating, rendering user's cart and finally a mock checkout page.
