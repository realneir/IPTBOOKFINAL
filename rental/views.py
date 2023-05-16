from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book, RentalTransaction


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def rent_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        num_days = int(request.POST.get('num_days'))
        rental_price = book.price_per_day * num_days

        if RentalTransaction.objects.filter(user=request.user).count() >= 3:
            message = "You have reached the maximum number of book rentals."
        else:
            transaction = RentalTransaction(user=request.user, book=book)
            transaction.save()
            message = f"Book '{book.title}' rented for {num_days} days. Total cost: ${rental_price}"
    else:
        message = None
    return render(request, 'rental/rent_book.html', {'book': book, 'message': message})


@login_required
def view_transactions(request):
    transactions = RentalTransaction.objects.all()
    return render(request, 'admin/view_transactions.html', {'transactions': transactions})
