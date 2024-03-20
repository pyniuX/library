from typing import Any

from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView

from .models import Person


class UserAddView(CreateView):
    template_name = "library/user_add.html"
    model = Person

    fields = ["name", "second_name", "surname", "birth_date"]

    def get_id():
        return Person.objects.last().id + 1


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


def user_status(request, person_id):
    user = get_object_or_404(Person, pk=person_id)
    context = {"user": user}
    return render(request, "library/user_status.html", context)


# def user_delete(request, person_id):
#     user = get_object_or_404(Person, pk=person_id)
#     user.is_active = False
#     user.save()
#     return render(request, "library/users.html")


def books(request):
    return render(request, "library/index.html")


def rents(request):
    return render(request, "library/index.html")
