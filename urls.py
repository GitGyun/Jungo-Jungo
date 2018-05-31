from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('product/', views.productpage, name='product'),
    path('searchpage/', views.productpage, name='searchpage'),
]