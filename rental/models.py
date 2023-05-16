from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    rental_days = models.PositiveIntegerField()
    rental_price = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
