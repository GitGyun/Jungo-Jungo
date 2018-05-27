from django.db import models

class Student(models.Model):
    sid = models.PositiveIntegerField(max_length=8)
    username = models.CharField(max_length=50)
    phone_no = models.PositiveIntegerField(max_length=10)
    email = models.CharField(max_length=100)
    balance = models.PositiveIntegerField()
