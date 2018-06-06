from django import forms
from .models import *
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

    def create_wishlist(self, author):
        if self.is_valid():
            # Make a new Product object.
            newprod = Product.objects.create(
                pname=self.cleaned_data['prodName'],
                prodType=self.cleaned_data['prodtype'],
                price=self.cleaned_data['price'],
                pdesc=self.cleaned_data['prodDesc'],
                author = author
            )
            
            # Make a new Wishlist object.
            row = Wishlist.objects.create(product=newprod)
            
            return row;

    def create_selllist(self, author):
        if self.is_valid():
            # Make a new Product object.
            newprod = Product.objects.create(
                pname=self.cleaned_data['prodName'],
                prodType=self.cleaned_data['prodtype'],
                price=self.cleaned_data['price'],
                pdesc=self.cleaned_data['prodDesc'],
                author = author
            )
            
            # Make a new Wishlist object.
            row = Selllist.objects.create(product=newprod)
            
            return row;
            
    def save(self, pid):
        if self.is_valid():
            prod = Product.objects.get(pid=pid)
            prod.pname = self.cleaned_data['prodName']
            prod.prodType=self.cleaned_data['prodtype']
            prod.price=self.cleaned_data['price']
            prod.pdesc=self.cleaned_data['prodDesc']
            prod.save()
                

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
            if self.cleaned_data['typeFilter'] == '0':
               qset = Wishinfo.objects.filter(
                    price__lte=self.cleaned_data['priceHi'],
                    price__gte=self.cleaned_data['priceLo'],
                    pname__contains=self.cleaned_data['nameFilter'],
                )
            else:
                qset = Wishinfo.objects.filter(
                    price__lte=self.cleaned_data['priceHi'],
                    price__gte=self.cleaned_data['priceLo'],
                    pname__contains=self.cleaned_data['nameFilter'],
                    prodType=self.cleaned_data['typeFilter'],
                )
            return qset;

    def find_in_selllist(self):
        if self.is_valid():
            if self.cleaned_data['typeFilter'] == '0':
                    qset = Sellinfo.objects.filter(
                    price__lte=self.cleaned_data['priceHi'],
                    price__gte=self.cleaned_data['priceLo'],
                    pname__contains=self.cleaned_data['nameFilter'],
                )
            else:
                qset = Sellinfo.objects.filter(
                    price__lte=self.cleaned_data['priceHi'],
                    price__gte=self.cleaned_data['priceLo'],
                    pname__contains=self.cleaned_data['nameFilter'],
                    prodType=self.cleaned_data['typeFilter'],
                )
            return qset;
            

class Edit_LoginForm(forms.Form):
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

    def edit_login(self,id1):
        if self.is_valid():
            Student1 = Student.objects.filter(student_id=id1)
            # Make a new Product object.
            for each_student in Student1:
                each_student.set_password(self.cleaned_data['password'])
                each_student.email = self.cleaned_data['email']
                each_student.phone_no = self.cleaned_data['phone_no']
                each_student.save()
            return each_student
