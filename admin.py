from django.contrib import admin
from .models import User, Category, Subcategory, Image, Cart, Order, Address, Wishlist, Payment, Feedback, ContactUs

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(ContactUs)
