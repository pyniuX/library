from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView

from .models import Person


class UserAddView(CreateView):
    template_name = "library/user_add.html"
    model = Person

    fields = ["name", "second_name", "surname", "birth_date"]


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


def user_delete(request):
    return render(request, "library/user_delete.html")


def books(request):
    return render(request, "library/index.html")


def rents(request):
    return render(request, "library/index.html")
