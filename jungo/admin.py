from django.contrib import admin

# Register your models here.
from .models import Product, Wishlist, Selllist, Matchlist

admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Selllist)
admin.site.register(Matchlist)
