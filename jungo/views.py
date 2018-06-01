from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, SearchField, NewProdForm
from .models import Student, Wishlist, Selllist, Matchlist, Product
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
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
                return mainpage(request)
            else:
                return HttpResponse('로그인 실패, 다시 시도 해보세요.')
    
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'jungo/login.html', context)


# Retrun Main Page of the Site with authenticated user information.
def mainpage(request):
    if request.user.is_authenticated:
        # Superuser.
        if request.user.is_superuser:
            return render(request, 'jungo/mainpage.html', {'username': Superuser})
            
        
        curr_user = Student.objects.get(username=request.user.username)
        context = {
            'username': curr_user.username
        }
        return render(request, 'jungo/mainpage.html', context)
    
    else:
        return login(request)

def mypage(request):
    if request.user.is_authenticated:
        current_user = Student.objects.get(username=request.user.username)
        context = {
            'userinfo': Student.objects.filter(username=request.user.username).values(
                                'username', 'student_id', 'email', 'phone_no', 'balance')[0],
            'wishinfo': current_user.wishlists.all(),
            'sellinfo': current_user.selllists.all(),
            'buyreq': current_user.matchlists_buyer.all(),
            'sellreq': current_user.matchlists_seller.all(),
        }
        return render(request, 'jungo/mypage.html', context)
    
    else:
        HttpResponse("You're not logged in!")

    
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
    
    return mainpage(request)


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
    
    return mainpage(request)


# Edit a post with NewProdForm.
def post_edit(request, pk):
    post = Product.objects.get(pid=pk)
    #post = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = NewProdForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = NewProdForm()
        return render(request, 'jungo/post_edit.html', {'form': form})


# Edit a post in the Selllist with NewProdForm.
def sell_post_edit(request, pk):
    post = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = NewProdForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('sell_post_detail', pk=post.pk)
    else:
        form = NewProdForm(instance=post)
        return render(request, 'jungo/sell_post_edit.html', {'form': form})
        

# Remove a post.
def post_remove(request, pk):
    post = get_object_or_404(Product, pk=pk)
    post.delete()
    return redirect('wishlist')


# Remove a post in the Selllist.    
def sell_post_remove(request, pk):
    post = get_object_or_404(Product, pk=pk)
    post.delete()
    return redirect('selllist')


# Show details about a post in the Wishlist.
def wishlist_detail(request, pk):
    post = get_object_or_404(Product, pk=pk)
    return render(request, 'jungo/wishlist_detail.html', {'post': post})


# Show details about a post in the Selllist.
def selllist_detail(request, pk):
    post = get_object_or_404(Product, pk=pk)
    return render(request, 'jungo/selllist_detail.html', {'post': post})
    


# Write a new post in the Wishlist. 
def write_wishlist(request):
    curr_user = Student.objects.get(username=request.user.username)
    
    if request.method == "POST":
        prod_form = NewProdForm(request.POST)
        if prod_form.is_valid():
            row = prod_form.create_wishlist()
            row.buyer.add(curr_user)
            return redirect('mainpage')
            
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
            row = prod_form.create_selllist()
            row.seller.add(curr_user)
            return redirect('mainpage')
            
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
        posts = Wishlist.objects.all()
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
            posts = search_form.find_in_wishlist()
            context = {
                'search_form' : search_form,
                'posts' : posts,
                }
            return render(request, 'jungo/selllist.html', context)
            
    else:
        posts = Selllist.objects.all()
        search_form = SearchField()
        context = {
            'search_form': search_form,
            'posts' : posts,
        }
        return render(request, 'jungo/selllist.html', context)
