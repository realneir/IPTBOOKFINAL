from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Transaction
from .serializers import UserSerializer, BookSerializer, TransactionSerializer

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully.'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_books(request):
    books = Book.objects.filter(available=True)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def rent_books(request):
    user = get_object_or_404(User, id=request.data.get('user_id'))
    book_ids = request.data.get('book_ids', [])
    rental_days = request.data.get('rental_days', 0)
    books = Book.objects.filter(id__in=book_ids, available=True)[:3]
    rental_price = sum(book.price for book in books) * rental_days
    if len(books) != len(book_ids):
        return Response({'message': 'Some of the selected books are not available.'}, status=400)
    if len(books) > 3:
        return Response({'message': 'You can only borrow a maximum of 3 books.'}, status=400)
    transaction = Transaction.objects.create(user=user, rental_days=rental_days, rental_price=rental_price)
    transaction.books.set(books)
    for book in books:
        book.available = False
        book.save()
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data, status=201)

@api_view(['GET'])
def view_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=200)
