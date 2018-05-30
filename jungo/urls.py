from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),                # for index pages.
    path('signup/', views.signup, name='signup'),       # for signup pages.
    path('login/', views.login, name='login'),          # for login pages.
    path('mainpage/', views.mainpage, name='mainpage'), # for main pages.
]
