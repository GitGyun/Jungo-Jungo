from django.urls import path
from django.conf.urls import url
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$',  views.index, name='index'),
   	url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^mainpage/', views.mypage, name='mainpage'),
    url(r'^post/wishlist/(?P<pk>[0-9]+)/edit/$', views.wish_edit, name='wish_edit'),
    url(r'^post/selllist/(?P<pk>[0-9]+)/edit/$', views.sell_edit, name='sell_edit'),
    url(r'^post/wishlist/(?P<pk>\d+)/remove/$', views.wish_remove, name='wish_remove'),
    url(r'^post/selllist/(?P<pk>\d+)/remove/$', views.sell_remove, name='sell_remove'),
    #url(r'^post/detail/(?P<pk>[0-9]+)/$', views.prod_detail, name='prod_detail'),
    path('post/<prod_state>/<int:pid>', views.prod_detail, name='prod_detail'),
    url('wishlist/', views.get_wishlist, name='wishlist'),
    url('wishlist_new/', views.write_wishlist, name='wishlist_new'),
    url('selllist/', views.get_selllist, name='selllist'),
    url('selllist_new/', views.write_selllist, name='selllist_new'),
    path('sell/<int:pid>', views.sell, name='sell'),
    path('buy/<int:pid>', views.buy, name='buy'),
    path('mypage/', views.mypage, name='mypage'),
    path('userinfo/<username>', views.userinfo, name='userinfo'),
    path('editinfo/', views.edit_login, name='editinfo'),
    path('complete/<int:pid>', views.complete, name='complete'),
    path('cancel/<int:pid>', views.cancel, name='cancel')
]
