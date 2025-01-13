from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # get the current session key if exits
        cart = self.session.get('session_key')

        # if the user is new , no session key ! create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} 
            
        # make sure cart is avalalble on all pages

        self.cart = cart

    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            #self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

        # Deal with loggied in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # converting {'3':2,'5':2} to {"3":2,"5":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile model
            current_user.update(old_cart= str(carty))

    def add(self,product, quantity):
        # creating session dictionary here of product id and quantity
    
        # now we have quantity also
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            #self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

        # Deal with loggied in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # first convert cart dicationary keys with double quotation.
            # converting {'3':2,'5':2} to {"3":2,"5":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile model
            current_user.update(old_cart= str(carty))

    

    def cart_total(self):
        # get product ids, here self.cart is the dictionary with {'2':3, '1':4} where key is productid and value is quantity 
        product_ids = self.cart.keys()
        # use ids to look up products in db
        products = Product.objects.filter(id__in=product_ids)
        # start count with Zeroprice
        total = 0
        # iterate over each product in cart
        # self.cart is dictionary : {'2':1,"3":1,"4":1,"5":1,"6":3}
        for key, value in self.cart.items():
            # convert key into integer for mathematical
            key = int(key)
            # get product from db
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                    # add price to total
                        total = total + (product.price * value)


        return total


    def __len__(self):
        return len(self.cart)
    

    # function to look up stuff in cart
    def get_prods(self):
        # Get Ids form cart 
        product_ids = self.cart.keys()
        # use ids to look up products in db
        products = Product.objects.filter(id__in=product_ids)
        # return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #  get cart
        ourcart=self.cart
        # update dictionary/cart
        ourcart[product_id] = product_qty
        # update session
    
        self.session.modified = True
        
        # Deal with loggied in user for cart persistence
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # converting {'3':2,'5':2} to {"3":2,"5":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile model
            current_user.update(old_cart= str(carty))

        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)
        # Delete from the dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        # update session i.e updating cart
        self.session.modified = True

        # Deal with loggied in user for cart persistence
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # converting {'3':2,'5':2} to {"3":2,"5":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile model
            current_user.update(old_cart= str(carty))
