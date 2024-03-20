from django.urls import path
from library import views

from .models import Person

app_name = "library"
urlpatterns = [
    path("", views.index, name="index"),
    path("people/", views.people, name="people"),
    path("people/authors/", views.authors, name="authors"),
    path("people/users/", views.users, name="users"),
    path(
        "people/users/add/",
        views.UserAddView.as_view(success_url=f"../{Person.objects.last().id+1}/"),
        name="user_add",
    ),
    path("people/users/<int:person_id>/", views.user_status, name="user_status"),
    # path("people/users/delete/", views.user_delete, name="user_delete"),
    path("books/", views.books, name="books"),
    path("rents/", views.rents, name="rents"),
]
# TODO: Person.objects.last is working only first time
