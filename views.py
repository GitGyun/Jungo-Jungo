from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.template import RequestContext
from .models import *
from django.http import HttpResponse


def index(request):
    return render(request, 'jungo/index.html')


def signup(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.signup()
            return redirect('index')
    else:
        signup_form = SignupForm()
        context = {
            'signup_form': signup_form,
        }
        return render(request, 'jungo/signup.html', context)
        
def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect('mainpage')
            else:
                return HttpResponse('<script> alert("Login Failed. Please Try Again"); history.back(-1);</script> ')
    
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'jungo/login.html', context)

def mainpage(request):
    if request.method == "POST":
        search_form = SearchField(request.POST)
        if search_form.is_valid():
            search_form.find()
            return redirect('searchpage')
    else:
        search_form = SearchField()
        context = {
            'search_form': search_form,
        }
        return render(request, 'jungo/search.html', context)
    # for testing : this block should go to productpage()
    #print("Size of table <Product> : " + str(Product.objects.count())) 
    #print(Product.objects.all());
    #if request.method == "POST":
    #    prod_form = NewProdForm(request.POST)
    #    if prod_form.is_valid():
    #        prod_form.create()
    #        return redirect('mainpage')
    ##else:
    #    prod_form = NewProdForm()
    #    context = {
    #        'prod_form': prod_form,
    #    }
    #    return render(request, 'jungo/product.html', context)

    ###
    
    # return render(request, 'jungo/mainpage.html')
        

def productpage(request):
    # print("Size of table <Product> : " + str(Product.objects.count())) 
    if request.method == "POST":
        prod_form = NewProdForm(request.POST)
        if prod_form.is_valid():
            prod_form.create()
            return redirect('mainpage')
    else:
        prod_form = NewProdForm()
        context = {
            'prod_form': prod_form,
        }
        return render(request, 'jungo/product.html', context)

def searchpage(request):
    if request.method == "POST":
        search_form = SearchField(request.POST)
        if search_form.is_valid():
            search_form.find()
            return redirect('searchpage')
    else:
        search_form = SearchField()
        context = {
            'search_form': search_form,
        }
        return render(request, 'jungo/search.html', context)
