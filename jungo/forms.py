from django import forms
from .models import Student, Product, Wishlist, Selllist
from .choices import *

class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    student_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    phone_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

# 자신이 가진 username과 password를 사용해서 유저 생성 후 반환하는 메서드
    def signup(self):
        if self.is_valid():
            return Student.objects.create_user(
                username=self.cleaned_data['username'],
                student_id=self.cleaned_data['student_id'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
                phone_no=self.cleaned_data['phone_no'],
                balance = 0,
            )

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class NewProdForm(forms.Form):
    prodName = forms.CharField(
    widget = forms.TextInput(
        attrs={
                'class': 'form-control',
              }
        )
    )
    prodtype = forms.ChoiceField(label="",
                                initial='',
                                widget=forms.Select(),
                                required=True, choices=STATUS_CHOICES)
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'class':'form-control',}
            )
        )
    prodDesc = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'class':'form-control',}
            )
        )

    def create_wishlist(self):
        if self.is_valid():
            # Make a new Product object.
            newprod = Product.objects.create(
                pname=self.cleaned_data['prodName'],
                prodType=self.cleaned_data['prodtype'],
                price=self.cleaned_data['price'],
                #pdesc=self.cleaned_data['prodDesc']
            )
            
            # Make a new Wishlist object.
            row = Wishlist.objects.create(product=newprod)
            
            return row;

    def create_selllist(self):
        if self.is_valid():
            # Make a new Product object.
            newprod = Product.objects.create(
                pname=self.cleaned_data['prodName'],
                prodType=self.cleaned_data['prodtype'],
                price=self.cleaned_data['price'],
                #pdesc=self.cleaned_data['prodDesc']
            )
            
            # Make a new Wishlist object.
            row = Selllist.objects.create(product=newprod)
            
            return row;


class SearchField(forms.Form):
    nameFilter = forms.CharField(required=False,
    widget = forms.TextInput(
        attrs={
                'class': 'form-control',
              }
        )
    )
    typeFilter = forms.ChoiceField(label="",
                                initial='',
                                widget=forms.Select(),
                                required=True, choices=STATUS_CHOICES_B)
    priceLo = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'class':'form-control',}
            )
        )
    priceHi = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'class':'form-control',}
            )
        )

    def find_in_wishlist(self):
        if self.is_valid():
            qset = Wishlist.objects.filter(
                product__price__lte=self.cleaned_data['priceHi'],
                product__price__gte=self.cleaned_data['priceLo'],
                product__pname__contains=self.cleaned_data['nameFilter'],
                product__prodType=self.cleaned_data['typeFilter'],
            )
            return qset;

    def find_in_selllist(self):
        if self.is_valid():
            qset = Selllist.objects.filter(
                product__price__lte=self.cleaned_data['priceHi'],
                product__price__gte=self.cleaned_data['priceLo'],
                product__pname__contains=self.cleaned_data['nameFilter'],
                product__prodType=self.cleaned_data['typeFilter'],
            )
            return qset;
