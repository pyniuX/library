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
    users_list = Person.objects.active()
    context = {"users_list": users_list}
    return render(request, "library/users.html", context)


def books(request):
    return render(request, "library/index.html")


def rents(request):
    return render(request, "library/index.html")
