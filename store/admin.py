from django.contrib import admin
from django.contrib.auth.models import User
from . models import Category,Customer,Product, Order, Profile

admin.site.register(Category)
admin.site.register(Customer)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name' , 'price' ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Profile)

# Mix profile info and  user info on same admin page
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
    # Add all the field which you want in your user admin
    model = User
    # field which you want from user model
    field = ["username","first_name","last_name","email"]
    # All the field from profile model
    inlines =[ProfileInline]

# unregister the old way
admin.site.unregister(User)
# Re-register the new way
admin.site.register(User,UserAdmin)

