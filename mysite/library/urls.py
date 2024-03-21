from django.urls import path
from library import views

from .models import Person

app_name = "library"
urlpatterns = [
    path("", views.index, name="index"),
    path("people/", views.people, name="people"),
    path("people/authors/", views.authors, name="authors"),
    path(
        "people/authors/add/",
        views.AuthorAddView.as_view(success_url=f"../"),
        name="author_add",
    ),
    path("people/authors/<int:person_id>/", views.author_status, name="author_status"),
    path("people/users/", views.users, name="users"),
    path(
        "people/users/add/",
        views.UserAddView.as_view(success_url=f"../"),
        name="user_add",
    ),
    path("people/users/<int:person_id>/", views.user_status, name="user_status"),
    path("people/users/<int:person_id>/delete/", views.user_delete, name="user_delete"),
    path("books/", views.books, name="books"),
    path("books/<int:book_id>/", views.book_status, name="book_status"),
]
