from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, SearchField, NewProdForm, Edit_LoginForm
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from django.utils import timezone
from django.http import HttpResponse


# Show the first page of the site.
def index(request):
    return render(request, 'jungo/index.html')


# Create a new user with SignupForm. 
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
 
       
# Authenticate user with LoginForm.        
def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                return mypage(request)
            else:
                return HttpResponse('로그인 실패, 다시 시도 해보세요.')
    
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'jungo/login.html', context)


# Logout user.
def logout(request):
    django_logout(request)
    return render(request, 'jungo/index.html')


# Show user information and trade information.
def mypage(request):
    if request.user.is_authenticated:
        context = {
            'userinfo': Userinfo.objects.get(username=request.user.username),
            'wishinfo': Wishinfo.objects.filter(username=request.user.username),
            'sellinfo': Sellinfo.objects.filter(username=request.user.username),
            'buyerinfo': Matchinfo.objects.filter(sellername=request.user.username),
            'sellerinfo': Matchinfo.objects.filter(buyername=request.user.username),
        }
        return render(request, 'jungo/mypage.html', context)
    
    else:
        return login(request)

    
# Sell a product from the Wishlist.    
def sell(request, pid):
    current_user = Student.objects.get(username=request.user.username)
    row = Wishlist.objects.get(product=pid)
    
    # User can't buy and sell himself/herself.
    buyer = row.buyer.all()[0]
    if buyer == current_user:
        return HttpResponse("You can't sell your wishing product!")
    
    # Create a row in the Matchlist.
    match = Matchlist(product=row.product)
    match.save()
    match.buyer.add(buyer)
    match.seller.add(current_user)
    
    # delete the product from the Wishlist.
    row.delete()
    
    return mypage(request)


# Buy a proudct from the Selllist.
def buy(request, pid):
    current_user = Student.objects.get(username=request.user.username)
    row = Selllist.objects.get(product=pid)
    
    # User can't buy and sell himself/herself.
    seller = row.seller.all()[0]
    if seller == current_user:
        return HttpResponse("You can't buy your selling product!")
    
    # Create a row in the Matchlist.
    match = Matchlist(product=row.product)
    match.save()
    match.seller.add(seller)
    match.buyer.add(current_user)
    
    # delete the product from the Wishlist.
    row.delete()
    
    return mypage(request)


# Edit a post in the Wishlist with NewProdForm.
def wish_edit(request, pk):
    if request.method == "POST":
        form = NewProdForm(request.POST)
        if form.is_valid():
            form.save(pk)
            return render(request, 'jungo/mypage.html', {'form': form})
            
    else:
        form = NewProdForm()
        return render(request, 'jungo/wish_edit.html', {'form': form})
        

# Edit a post in the Selllist with NewProdForm.
def sell_edit(request, pk):
    if request.method == "POST":
        form = NewProdForm(request.POST)
        if form.is_valid():
            form.save(pk)
            return render(request, 'jungo/mypage.html', {'form': form})

    else:
        form = NewProdForm()
        return render(request, 'jungo/sell_edit.html', {'form': form})
        

# Remove a post in the Wishlist.
def wish_remove(request, pk):
    post = Product.objects.get(pk=pk)
    post.delete()
    return redirect('wishlist')


# Remove a post in the Selllist.    
def sell_remove(request, pk):
    post = Product.objects.get(pk=pk)
    post.delete()
    return redirect('selllist')


# Show details about a post.
def prod_detail(request, pid, prod_state):
    post = Product.objects.get(pid=pid)
    if prod_state == 'wishlist':
        wisher = Wishinfo.objects.get(pid=pid).username
        context = {
            'post': post,
            'wisher': wisher,
            'prod_state': 'wishlist'
        }
    elif prod_state == 'selllist':
        seller = Sellinfo.objects.get(pid=pid).username
        context = {
            'post': post,
            'seller': seller,
            'prod_state': 'selllist'
        }
    else:
        buyer = Matchinfo.objects.get(pid=pid).buyername
        seller = Matchinfo.objects.get(pid=pid).sellername
        context = {
            'post': post,
            'buyer': buyer,
            'seller': seller,
            'prod_state': 'matchlist'
        }
    return render(request, 'jungo/prod_detail.html', context)
    

# Write a new post in the Wishlist. 
def write_wishlist(request):
    curr_user = Student.objects.get(username=request.user.username)
    
    if request.method == "POST":
        prod_form = NewProdForm(request.POST)
        if prod_form.is_valid():
            row = prod_form.create_wishlist(curr_user)
            row.buyer.add(curr_user)
            return redirect('mypage')
            
    else:
        prod_form = NewProdForm()
        context = {
            'prod_form': prod_form,
            'buyer_id': curr_user.username,
        }
        return render(request, 'jungo/wishlist_new.html', context)


# Write a new post in the Selllist. 
def write_selllist(request):
    curr_user = Student.objects.get(username=request.user.username)
    
    if request.method == "POST":
        prod_form = NewProdForm(request.POST)
        if prod_form.is_valid():
            row = prod_form.create_selllist(curr_user)
            row.seller.add(curr_user)
            return redirect('mypage')
            
    else:
        prod_form = NewProdForm()
        context = {
            'prod_form': prod_form,
            'buyer_id': curr_user.username,
        }
        return render(request, 'jungo/selllist_new.html', context)


# Show the Wishlist and provide search service.
def get_wishlist(request):
    if request.method == "POST":
        search_form = SearchField(request.POST)
        if search_form.is_valid():
            posts = search_form.find_in_wishlist()
            context = {
                'search_form': search_form,
                'posts': posts,
                }
            return render(request, 'jungo/wishlist.html', context)
            
    else:
        posts = Wishinfo.objects.all()
        search_form = SearchField()
        context = {
            'search_form': search_form,
            'posts' : posts,
        }
        return render(request, 'jungo/wishlist.html', context)


# Show the Selllist and provide search service.
def get_selllist(request):
    if request.method == "POST":
        search_form = SearchField(request.POST)
        if search_form.is_valid():
            posts = search_form.find_in_selllist()
            context = {
                'search_form': search_form,
                'posts': posts,
                }
            return render(request, 'jungo/selllist.html', context)
            
    else:
        posts = Sellinfo.objects.all()
        search_form = SearchField()
        context = {
            'search_form': search_form,
            'posts': posts,
        }
        return render(request, 'jungo/selllist.html', context)


# Show user information.
def userinfo(request, username):
    info = Userinfo.objects.get(username=username)
    context = {
        'userinfo': info
    }
    return render(request, 'jungo/userinfo.html', context)


# Edit user information.
def edit_login(request):
    current_user = Student.objects.get(username=request.user.username)
    if request.method == "POST":
        edit_signup_form = Edit_LoginForm(request.POST)
        if edit_signup_form.is_valid():
            edit_signup_form.edit_login(current_user.student_id)
            return mypage(request)
    else:
        edit_signup_form = Edit_LoginForm()
        context = {
            'signup_form': edit_signup_form,
        }
        return render(request, 'jungo/edit_login.html', context) 


# Complete or Cancel the trade.
def cancel(request, pid):
    curr_user = Student.objects.get(username=request.user.username)
    
    # Re-insert the product into Wishlist/Selllist.
    info = Matchinfo.objects.get(pid=pid)
    prod = Product.objects.get(pid=pid)
    
    # User is buyer.
    if curr_user.username == info.buyername:
        # The product was in Wishlist.
        if prod.author.username == curr_user.username:
            row = Wishlist(product=prod)
            row.save()
            row.buyer.add(curr_user)
            
        # The product was in Selllist.
        else:
            seller = Student.objects.get(username=info.sellername)
            row = Selllist(product=prod)
            row.save()
            row.seller.add(seller)
    
    # User is seller.
    else:
        # The product was in Selllist.
        if prod.author.username == curr_user.username:
            row = Selllist(product=prod)
            row.save()
            row.seller.add(curr_user)
            
        # The product was in Selllist.
        else:
            buyer = Student.objects.get(username=info.buyername)
            row = Wishlist(product=prod)
            row.save()
            row.buyer.add(buyer)
             
    
    # Delete the product from Matchlist.
    match = Matchlist.objects.get(product_id=pid)
    match.delete()
    
    return mypage(request)
    

# Complete the trade.
def complete(request, pid):
    prod = Product.objects.get(pid=pid)
    prod.pstate += 1
    prod.save()
    
    if prod.pstate == 2:
        prod.delete()
    
    return mypage(request)
