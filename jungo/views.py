from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from .models import Student, Wishlist, Selllist, Matchlist
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.template import RequestContext

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
                return mainpage(request)
            else:
                return HttpResponse('로그인 실패, 다시 시도 해보세요.')
    
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'jungo/login.html', context)


def mainpage(request):
    current_user = Student.objects.get(username=request.user.username)
    if current_user.is_authenticated:
        context = {
            'userinfo': Student.objects.filter(username=request.user.username).values(
                                'username', 'student_id', 'email', 'phone_no', 'balance')[0],
            'wishinfo': current_user.wishlists.all(),
            'sellinfo': current_user.selllists.all(),
            'buyreq': current_user.matchlists_buyer.all(),
            'sellreq': current_user.matchlists_seller.all(),
        }
        return render(request, 'jungo/mainpage.html', context)
    
    else:
        return login(request)


def wishlist(request):
    context = {
        'wishlist': Wishlist.objects.all()
    }
    return render(request, 'jungo/wishlist.html', context)
    
    
def sell(request, pid):
    current_user = Student.objects.get(username=request.user.username)
    row = Wishlist.objects.get(product=pid)
    
    # Create a row in the Matchlist.
    match = Matchlist(product=row.product)
    match.save()
    match.buyer.add(row.buyer.all()[0])
    match.seller.add(current_user)
    
    # delete the product from the Wishlist.
    row.delete()
    
    return mainpage(request)
