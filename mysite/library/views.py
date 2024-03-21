from typing import Any

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from .models import Person


class UserAddView(CreateView):
    template_name = "library/user_add.html"
    model = Person

    fields = ["name", "second_name", "surname", "birth_date"]


class AuthorAddView(CreateView):
    template_name = "library/author_add.html"
    model = Person

    fields = ["name", "second_name", "surname", "birth_date", "death_date", "is_active"]


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
    users_list = Person.objects.active().annotate_opened_rents_number()[:15]
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
    return render(request, "library/index.html")


def rents(request):
    return render(request, "library/index.html")
