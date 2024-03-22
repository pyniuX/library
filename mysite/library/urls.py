from django.urls import path
from library import views

from .models import Person

app_name = "library"
urlpatterns = [
    path("", views.index, name="index"),
    path("people/", views.people, name="people"),
    path("people/authors/", views.authors, name="authors"),
    # path(
    #     "people/authors/add/",
    #     views.AuthorAddView.as_view(success_url="../"),
    #     name="author_add",
    # ),
    path("people/authors/add/", views.author_add, name="author_add"),
    path("people/authors/<int:person_id>/", views.author_status, name="author_status"),
    path("people/users/", views.users, name="users"),
    path(
        "people/users/add/",
        views.UserAddView.as_view(success_url="../"),
        name="user_add",
    ),
    path("people/users/<int:person_id>/", views.user_status, name="user_status"),
    path("people/users/<int:person_id>/delete/", views.user_delete, name="user_delete"),
    path("books/", views.books, name="books"),
    # path(
    #     "books/add/",
    #     views.BookAddView.as_view(success_url="../"),
    #     name="book_add",
    # ),
    path("books/add/", views.book_add, name="book_add"),
    path("books/<int:book_id>/", views.book_status, name="book_status"),
    path("books/<int:book_id>/delete/", views.book_delete, name="book_delete"),
    path("rents/", views.rents, name="rents"),
    path(
        "rents/add/",
        views.RentAddView.as_view(success_url="../"),
        name="rent_add",
    ),
    path("rents/<int:rent_id>/", views.rent_status, name="rent_status"),
    path("rents/<int:rent_id>/return/", views.rent_return, name="rent_return"),
]
