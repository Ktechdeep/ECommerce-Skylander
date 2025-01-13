from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm , PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime

# Create your views here.

def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:

        # Get the order using primary key
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        # if form filled
        if request.method == 'POST':
            # get the status
            status = request.POST['shipping_status'] # coming from order.html form
            # check if true or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # update the status
                order.update(shipped=False)     

            messages.success(request,"shipping status updated")
            return redirect('home')

        return render(request, 'payment/orders.html',{"order": order, "items": items})

    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:

        orders = Order.objects.filter(shipped=False)

        # if form filled
        if request.method == 'POST':
            # get the status
            status = request.POST['shipping_status'] # coming from order.html form
            num = request.POST['num']
            # Get the order
            order =Order.objects.filter(id=num)
            # grab date and time
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)   

            messages.success(request,"shipping status updated")
            return redirect('home')

        return render(request, 'payment/not_shipped_dash.html', {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        # if form filled
        if request.method == 'POST':
            # get the status
            status = request.POST['shipping_status'] # coming from order.html form
            num = request.POST['num']

            # Get the order
            order=Order.objects.filter(id=num)

            # grab date and time
            now = datetime.datetime.now()
            order.update(shipped=False)   

            messages.success(request,"shipping status updated")
            return redirect('home')



        return render(request, 'payment/shipped_dash.html', {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def process_order(request):
    if request.POST: # if form submitted 

        # Get the cart
        cart= Cart(request)
        cart_products = cart.get_prods # getting products to display on the cart summary page
        quantites = cart.get_quants # getting quantity to visible on cart summary
        totals = cart.cart_total() # getting total quantity
    
        # Get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping session Data which is dictionary of shipping info
        my_shipping = request.session.get('my_shipping')
        
        # Gather Order information as per "order model"
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email'] 
        # Create Shipping Address from Session info
        shipping_address= f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals



        # Create an Order
        if request.user.is_authenticated:
            # logged in user            
            user = request.user

            # Create Order with user detail
            create_order = Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()


            # Add order items
            # Get the order ID
            order_id = create_order.pk
            # get product information
            for product in cart_products():
                # get product id
                product_id = product.id
                # get product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price
                # get quantity
                for key, value in quantites().items():
                    if int(key) == product_id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value,price=price)
                        create_order_item.save()

            # Delete our cart once order shipped, by just deleteing session data
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete the key
                    del request.session[key]
                    
            # Delete cart from database(old_cart field)
            current_user = Profile.objects.filter(user__id = request.user.id)
            # delete shopping cart in database(old_cart field)
            current_user.update(old_cart="")
            
            messages.success(request,"Order Placed!")
            return redirect('home')

        else:
            # not logged in user
            # Create Order without user detail
            create_order = Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk
            # get product information
            for product in cart_products():
                # get product id
                product_id = product.id
                # get product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price
                # get quantity
                for key, value in quantites().items():
                    if int(key) == product_id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value,price=price)
                        create_order_item.save()
                        
            # Delete our cart once order shipped, by just deleteing session data
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete the key
                    del request.session[key]

            
            messages.success(request,"Order Placed!")
            return redirect('home')

    else:
        messages.success(request,"Acess Denied")
        return redirect('home')
    

def billing_info(request):

    # if come from previouspage
    if request.POST:
        
        # get the cart information
        cart= Cart(request)
        cart_products = cart.get_prods # getting products to display on the cart summary page
        quantites = cart.get_quants # getting quantity to visible on cart summary
        totals = cart.cart_total # getting total quantity

        # create a session with Shipping information
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products":cart_products , "quantites":quantites, "totals":totals, 'shipping_info':request.POST, 'billing_form':billing_form})
            
        else:
            # not logged in
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products":cart_products , "quantites":quantites, "totals":totals, 'shipping_info':request.POST, 'billing_form':billing_form})

        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products":cart_products , "quantites":quantites, "totals":totals, 'shipping_form':shipping_form})
    
    else:
        messages.success(request,"Access denied")
        return redirect('home')


def checkout(request):
    cart= Cart(request)
    cart_products = cart.get_prods # getting products to display on the cart summary page
    quantites = cart.get_quants # getting quantity to visible on cart summary
    totals = cart.cart_total # getting total quantity


    if request.user.is_authenticated:
        # checkout as loggedin user
        # shipping user
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        # shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user ) # form name is <shipping_form>
        return render(request, 'payment/checkout.html', {"cart_products":cart_products , "quantites":quantites, "totals":totals, 'shipping_form':shipping_form,})
    else:
        # checkout as guest user
        shipping_form = ShippingForm(request.POST or None ) 
        return render(request, 'payment/checkout.html', {"cart_products":cart_products , "quantites":quantites, "totals":totals, 'shipping_form':shipping_form,})








def payment_success(request):
    return render(request, 'payment/payment_success.html',{})