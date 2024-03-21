from typing import Any

from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from .models import Book, Person, Rent


class UserAddView(CreateView):
    template_name = "library/user_add.html"
    model = Person
    fields = ["name", "second_name", "surname", "birth_date"]


class AuthorAddView(CreateView):
    template_name = "library/author_add.html"
    model = Person
    fields = ["name", "second_name", "surname", "birth_date", "death_date", "is_active"]


class BookAddView(CreateView):
    template_name = "library/book_add.html"
    model = Book

    fields = ["title", "authors"]


def index(request):
    return render(request, "library/index.html")


def people(request):
    return render(request, "library/people.html")


def authors(request):
    authors_list = Person.objects.authors()
    context = {"authors_list": authors_list}
    return render(request, "library/authors.html", context)


def author_status(request, person_id):
    author = get_object_or_404(Person, pk=person_id)
    context = {"author": author}
    return render(request, "library/author_status.html", context)


def users(request):
    users_list = Person.objects.active().annotate_opened_rents_number()
    context = {"users_list": users_list}
    return render(request, "library/users.html", context)


def user_status(request, person_id):
    user = get_object_or_404(Person, pk=person_id)
    context = {"user": user}
    return render(request, "library/user_status.html", context)


def user_delete(request, person_id):
    user = get_object_or_404(Person, pk=person_id)
    user.is_active = False
    user.save()
    return redirect("/library/people/users/")


def books(request):
    books_list = Book.objects.all().active().prefetch_related("authors")
    context = {"books_list": books_list}
    return render(request, "library/books.html", context)


def book_status(request, book_id):
    queryset = Book.objects.filter(id=book_id).status()
    book = get_object_or_404(queryset)

    context = {"book": book}
    return render(request, "library/book_status.html", context)


def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_active = False
    book.save()
    return redirect("/library/books/")
