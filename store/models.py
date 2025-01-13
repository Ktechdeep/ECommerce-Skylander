from django.db import models
import datetime
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create Customer profile
class Profile(models.Model):
    # associating one profile to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now_add=True)
    phone = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=200, blank = True)
    address2 = models.CharField(max_length=200, blank = True)
    city = models.CharField(max_length=200, blank = True)
    state = models.CharField(max_length=200, blank = True)
    zip_code = models.CharField(max_length=20, blank = True)
    country = models.CharField(max_length=200, blank = True)
    old_cart=  models.CharField(max_length=200, blank = True, null=True)
    def __str__(self):
        return self.user.username 
    
# Create a user Profile by default  when user signup form our register page
def create_profile(sender, instance, created, **kwargs):
    # if user is created
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)





# product catgories list
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True , null=True , blank=True)
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.name)
        super(Category ,self).save(*args , **kwargs)

    def __str__(self):
        return self.name
    
    # fix the name in admin site
    class Meta:
        verbose_name_plural = 'Categories'

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=250,default='' , blank=True, null=True)                  
    image = models.ImageField(upload_to='uploads/product/')
    slug = models.SlugField(unique=True  , null=True , blank=True)
    # Add sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True, null=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=100, default='' , blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product