from .cart import Cart

# Create context processor so our cart can work on all page of site

def cart(request):
    cart = Cart(request)
    return {'cart': cart}
