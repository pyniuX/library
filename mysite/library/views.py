from django.http import HttpResponse
from django.shortcuts import render

from .models import Person


def index(request):
    return render(request, "library/index.html")


def people(request):
    return render(request, "library/people.html")


def authors(request):
    return render(request, "library/index.html")


def users(request):
    users_list = Person.objects.active().annotate_opened_rents_number()[:15]
    context = {"users_list": users_list}
    return render(request, "library/users.html", context)


def user_add(request):
    return render(request, "library/index.html")


def user_delete(request):
    return render(request, "library/index.html")


def books(request):
    return render(request, "library/index.html")


def rents(request):
    return render(request, "library/index.html")
