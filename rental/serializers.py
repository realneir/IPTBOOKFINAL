from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['user', 'books', 'rental_days', 'rental_price', 'transaction_date']
