import datetime

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import AuthorForm, BookForm, BookInAuthorForm, LoginForm
from .models import Book, Person, Rent


class UserAddView(CreateView):
    template_name = "library/user_add.html"
    model = Person
    fields = ["name", "second_name", "surname", "birth_date"]


class RentAddView(CreateView):
    template_name = "library/rent_add.html"
    model = Rent

    fields = ["book", "user"]


class LoginView(LoginView):
    template_name = "library/login.html"
    next_page = reverse_lazy("library:index")
    form_class = LoginForm


# TODO: change na,e


class LogoutView(LogoutView):
    next_page = reverse_lazy("library:index")
    template_name = "library/index.html"


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
    books = Person.objects.get(id=person_id).book_set.values("title").distinct()
    context = {"author": author, "books": books}
    return render(request, "library/author_status.html", context)


def author_add(request):
    if request.method == "POST":
        author_form = AuthorForm(request.POST)
        book_form = BookInAuthorForm(request.POST)
        if book_form.is_valid() and author_form.is_valid():
            author = Person(
                name=author_form.cleaned_data["name"],
                second_name=author_form.cleaned_data["second_name"],
                surname=author_form.cleaned_data["surname"],
                birth_date=author_form.cleaned_data["birth_date"],
                death_date=author_form.cleaned_data["death_date"],
                is_active=author_form.cleaned_data["is_active"],
            )
            author.save()
            book = Book(title=book_form.cleaned_data["title"])
            book.save()
            book.authors.add(author.id)
            return redirect(reverse("library:authors"))
        else:
            author_form = AuthorForm(data=request.POST)
            book_form = BookInAuthorForm(data=request.POST)
            messages.error(request, "Wrong data, validation error, try again.")
            context = {"book_form": book_form, "author_form": author_form}
            return render(request, "library/author_add.html", context)
    else:
        author_form = AuthorForm()
        book_form = BookInAuthorForm()
        context = {"book_form": book_form, "author_form": author_form}
        return render(request, "library/author_add.html", context)


def book_add(request):
    if request.method == "POST":
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book = Book(title=book_form.cleaned_data["title"])
            book.save()
            for author in book_form.cleaned_data["authors"]:
                book.authors.add(author.id)
            return redirect(reverse("library:books"))
    else:
        book_form = BookForm()
        context = {"book_form": book_form}
        return render(request, "library/book_add.html", context)


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
    return redirect(reverse("library:users"))


def books(request):
    books = Book.objects.all().active().prefetch_related("authors").status()
    context = {"books": books}
    return render(request, "library/books.html", context)


def book_status(request, book_id):
    queryset = Book.objects.filter(id=book_id).status().prefetch_related("authors")
    book = get_object_or_404(queryset)
    context = {"book": book}
    return render(request, "library/book_status.html", context)


def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_active = False
    book.save()
    return redirect(reverse("library:books"))


def test(request):
    return HttpResponse("odpowiedz")


def rents(request):
    rents_list = (
        Rent.objects.all().prefetch_related("book", "user").order_by("return_date")
    )
    context = {"rents_list": rents_list}
    return render(request, "library/rents.html", context)


def rent_status(request, rent_id):
    queryset = Rent.objects.filter(id=rent_id).prefetch_related("book", "user")
    rent = get_object_or_404(queryset)
    context = {"rent": rent}
    return render(request, "library/rent_status.html", context)


def rent_return(request, rent_id):
    rent = get_object_or_404(Rent, pk=rent_id)
    rent.return_date = datetime.date.today()
    rent.save()
    return redirect(reverse("library:rents"))


# DONE:  w błedzie formularz nie powinien być zerowany
# DONE: lista ksiazek w authors ma byc wyswietlana w nowej lini bez przecinka w ostatnim(lub w ogóle bez)
# DONE: pouzywac nazw urlów
# DONE: logowanie  - link na chacie
# DONE: deployment django girls
# DONE: wyglad
# DONE: allowed host o co biega w końcu
# DONE: static files to root folder
# TODO: logout button
