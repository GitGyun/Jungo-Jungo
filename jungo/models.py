from django.db import models

class Student(models.Model):
    sid = models.PositiveIntegerField(max_length=8, primary_key=True)
    username = models.CharField(max_length=50)
    phone_no = models.PositiveIntegerField(max_length=10)
    email = models.CharField(max_length=100)
    balance = models.PositiveIntegerField()

class Product(models.Model):
    pid = models.PositiveIntegerField(max_length=8, primary_key=True)
    prodName = models.CharField(max_length=30)
    prodtype_choice = (
        ('A','Appliances'),
        ('B','Textbooks'),
        ('C','Vehicles'),
        ('D','Others'),
        )
    prodType = models.CharField(
        max_length=1,
        choices=prodtype_choice,
        default='A',
        )
    price = models.PositiveIntegerField()
    prodDesc = models.TextField()
    # prodState = models.PositiveIntegerField(max_length=1)

class SellList(models.Model):
    sellerID = models.ForeignKey(Student, on_delete=models.CASCADE)
    prodID = models.ForeignKey(Product, on_delete=models.CASCADE, primary_key=True)

class WishList(models.Model):
    wisherID = models.ForeignKey(Student, on_delete=models.CASCADE)
    prodID = models.ForeignKey(Product, on_delete=models.CASCADE, primary_key=True)

