from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),                                # index page.
    path('signup/', views.signup, name='signup'),                       # signup page.
    path('login/', views.login, name='login'),                          # login page.
    path('mainpage/', views.mainpage, name='mainpage'),                 # main page.
    path('mainpage/wishlist', views.wishlist, name='wishlist'),         # show wishlist.
    path('sell/<int:pid>', views.sell, name='sell'),                    # sell the product.
    path('mainpage/selllist', views.selllist, name='wishlist'),         # show wishlist.
    path('buy/<int:pid>', views.buy, name='buy'),                       # buy the product.
]
