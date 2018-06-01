from django.urls import path
from django.conf.urls import url
from . import views

from django.conf.urls.static import static
from django.conf import settings
'''
urlpatterns = [
    path('', views.index, name='index'),                                # index page.
    path('signup/', views.signup, name='signup'),                       # signup page.
    path('login/', views.login, name='login'),                          # login page.
    path('mainpage/', views.mainpage, name='mainpage'),                 # main page.
    path('sell/<int:pid>', views.sell, name='sell'),                    # sell the product.
    path('buy/<int:pid>', views.buy, name='buy'),                       # buy the product.
    
    url(r'^buypage/', views.buypage, name='buypage'),
    url(r'^sellpage/', views.sellpage, name='sellpage'), 
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
]
'''

urlpatterns = [
    url(r'^$',  views.index, name='index'),
   	url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login, name='login'),
    url(r'^mainpage/', views.mainpage, name='mainpage'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/wishlist/(?P<pk>[0-9]+)/$', views.wishlist_detail, name='wishlist_detail'),
    url(r'^post/selllist/(?P<pk>[0-9]+)/$', views.selllist_detail, name='selllist_detail'),
    url('wishlist/', views.get_wishlist, name='wishlist'),
    url('wishlist_new/', views.write_wishlist, name='wishlist_new'),
    url('selllist/', views.get_selllist, name='selllist'),
    url('selllist_new/', views.write_selllist, name='selllist_new'),
    path('sell/<int:pid>', views.sell, name='sell'),                    # sell the product.
    path('buy/<int:pid>', views.buy, name='buy'),                       # buy the product.
    path('mypage/', views.mypage, name='mypage')
]
