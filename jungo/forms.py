from django import forms
from django.contrib.auth.models import *
from jungo.choices import *
from jungo.models import *

class SignupForm(forms.Form):
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

# 자신이 가진 username과 password를 사용해서 유저 생성 후 반환하는 메서드
    def signup(self):
        if self.is_valid():
            return User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
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

    def create(self):
        if self.is_valid():
            return Product.objects.create(
                pid=Product.objects.count(),    
                prodName=self.cleaned_data['prodName'],
                prodType=self.cleaned_data['prodtype'],
                price=self.cleaned_data['price'],
                prodDesc=self.cleaned_data['prodDesc']
                )

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

    def find(self):
        if self.is_valid():
            qset = Product.objects.filter(
                price__lte=self.cleaned_data['priceHi'],
                price__gte=self.cleaned_data['priceLo'],
                prodName__contains=self.cleaned_data['nameFilter'],
                prodType=self.cleaned_data['typeFilter']
                );
            return qset;
