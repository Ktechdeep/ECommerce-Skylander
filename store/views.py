from django.shortcuts import render,redirect
from . models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm , UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def category(request, slug):
    # Grab the category by slug
    try:
        category = Category.objects.get(slug=slug)  # Use slug instead of name
        # Get all products in that category
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, 'Category does not exist!')
        return redirect('home')



def product(request,slug):
    try:
        product = Product.objects.get(slug = slug)
        return render(request, 'product.html', {'product': product})
    except Exception as e:
        print(e, 'Cateogry does not exist')


def home(request):
    products =  Product.objects.all()
    return render(request, 'home.html',{'products': products})

def about(request):
    return render(request, 'about.html',{ })

import json
from cart.cart import Cart
def login_user(request):
    # if user filled in login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        if user is not None: 
            login(request, user)

            # Do some shooping cart updating stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get there saved cart from database
            saved_cart = current_user.old_cart
            # convert database string to python dictionary
            if saved_cart:
                # conver to python dictionary using json
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary
                # Get the cart
                cart = Cart(request)
                # loop thorugh the cart and add the items form database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity = value)
                    






            messages.success(request, f'Welcome {username}!!')
            return redirect('home')
        else: # if user is not logged in
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def register_user(request):
    """
    Handle user registration process.

    This function manages the user registration process, including form validation,
    user creation, authentication, login, and sending a welcome email.

    Parameters:
    request (HttpRequest): The HTTP request object containing user submitted data.

    Returns:
    HttpResponse: Renders the registration page with the form if the request method
                  is GET or if the form is invalid. Redirects to the login page upon
                  successful registration.

    Side effects:
    - Creates a new user in the database if form is valid.
    - Logs in the newly created user.
    - Sends a welcome email to the user's provided email address.
    - Sets success or error messages in the request's session.
    """
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST) # form name is <form> here 
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)
            login(request, user)

            htmly = get_template('email.html')
            d = {'username': username,'password': password}
            subject, from_email, to = 'welcome', 'peedluek@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, f'Account created for {username}!!')
            return redirect('update_info')
        else:
            messages.error(request, 'Invalid form')
            return render(request,'register.html', {'form': form, 'error': 'Invalid form'})
    else:
        return render(request, 'register.html', {'form': form})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # if filled the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                # if you dont want to login again
                messages.success(request, 'Your password has been updated successfully!')
                login(request, current_user)
                return redirect('update_user')

                # if you want to login again
                messages.success(request, 'Your password has been updated successfully! Please login again.')
                return redirect('login')
            else:
                # Collect all the form errors in a list and display them to the user
                for errors in list(form.errors.values()):
                    messages.error(request, errors)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
        
    else:
        messages.success(request, 'You must be logged In !')
        return redirect('home')




def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user ) # form name is <user_form>
    
        # if user filled the form
        if user_form.is_valid():            
            user_form.save()
            
            login(request, current_user)
            messages.success(request, 'Your account has been updated successfully!')
            return redirect('home')

        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request,"you must be logged in")
        return redirect('home')


def update_info(request):
    
    if request.user.is_authenticated:
        # search for the user profile that has given user id 
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current user shipping information
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user ) # form name is <user_form>
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user ) # form name is <shipping_form>
    
        # if user filled the form
        if form.is_valid() or shipping_form.is_valid() :
            shipping_form.save()            
            form.save()
        
            
            messages.success(request, 'Your information has been updated successfully!')
            return redirect('home')

        return render(request, 'update_info.html', {'form': form, 'shipping_form':shipping_form, })
    else:
        messages.success(request,"you must be logged in")
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        # Get the search query from the form (use .get() to avoid KeyError)
        search_query = request.POST.get('searched', '').strip()

        if search_query:  # Check if the search query is not empty
            # Search for products with a case-insensitive name and discription match in the field of product model
            products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

            if products.exists():  # Check if any products were found
                return render(request, 'search.html', {'searched': products})
            else:
                messages.error(request, 'This product is not available, sorry for the inconvenience!')
        else:
            messages.warning(request, 'Please enter a valid search query.')
        
    # Render the search page with no results (GET or invalid POST)
    return render(request, 'search.html', {})
