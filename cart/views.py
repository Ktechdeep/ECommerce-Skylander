from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart= Cart(request)
    cart_products = cart.get_prods # getting products to display on the cart summary page
    quantites = cart.get_quants # getting quantity to visible on cart summary
    totals = cart.cart_total # getting total quantity
    return render(request, "cart_summary.html", {"cart_products":cart_products , "quantites":quantites, "totals":totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':
        # grabbing id and quantity
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) # this is the key "product_qty" given in ajax on product.html
        # look up product in db
        product  = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product, quantity = product_qty)

        # get card quantity

        cart_quantity = cart.__len__()

        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity}) # you cqn see this on console
        messages.success(request,'Product added to cart successfully')  # success
        return response

def cart_delete(request):
    # Get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # grabbing id 
        product_id = int(request.POST.get('product_id'))
        # call delete method from cart.py
        cart.delete(product=product_id)

        response = JsonResponse({'product_id': product_id})
    
        messages.success(request,'Product deleted from cart')  # success
        return response



    return render(request, 'cart_delete.html', {})

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # grabbing id and quantity
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) # this is the key "product_qty" given in ajax on cart_summary.html

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty, 'product_id': product_id})
        messages.success(request,'Cart updated succesfully')  # success
        return response
