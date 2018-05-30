from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),                # 첫 페이지들.
    path('signup/', views.signup, name='signup'),       # 회원가입을 위한 페이지들.
    path('login/', views.login, name='login'),          # 로그인을 위한 페이지들.
    path('mainpage/', views.mainpage, name='mainpage'), # 메인 페이지들.
]
