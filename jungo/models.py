from django.db import models
from django.contrib.auth.models import User

'''
A product for trade.
Generated by user, then put into the wishlist or the selllist.
'''
class Product(models.Model):
    pid = models.IntegerField(primary_key=True)             # product id.
    pname = models.CharField(max_length=16)                 # product name.
    ptype = models.CharField(max_length=1)                  # product type.
    price = models.IntegerField()                           # price of the product.
    pdesc = models.CharField(max_length=5000, null=True)    # description of the product.


'''
A wishlist for trade.
User who wishes to buy a product put it into the wishlist.
If someone wants to sell the product, it goes to the matchlist.
'''    
class Wishlist(models.Model):
    bid = models.ManyToManyField(User,
                                 related_name='%(app_label)s_%(class)s_bid') # id of the buyer.
    pid = models.OneToOneField(Product, primary_key=True, on_delete=True,
                               related_name='%(app_label)s_%(class)s_pid')   # pid of the product.


'''
A selllist for trade.
User who wishes to sell a product put it into the selllist.
If someone wants to buy the product, it goes to the matchlist.
'''    
class Selllist(models.Model):
    sid = models.ManyToManyField(User,
                                 related_name='%(app_label)s_%(class)s_sid') # id of the buyer.
    pid = models.OneToOneField(Product, primary_key=True, on_delete=True,
                               related_name='%(app_label)s_%(class)s_pid')   # pid of the product.
    

'''
A matchlist for trade.
If someone decided to trade a product in the wishlist or in the sellist,
the product and both buyer and seller put into the matchlist.
When the trade have been finished, the information is going to be deleted.
'''
class Matchlist(models.Model):
    bid = models.ManyToManyField(User,
                                 related_name='%(app_label)s_%(class)s_bid') # id of the buyer.
    sid = models.ManyToManyField(User,
                                 related_name='%(app_label)s_%(class)s_sid') # id of the buyer.
    pid = models.OneToOneField(Product, primary_key=True, on_delete=True,
                               related_name='%(app_label)s_%(class)s_pid')   # pid of the product.
