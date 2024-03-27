from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from library import views

app_name = "library"
urlpatterns = [
    path("", login_required(views.index), name="index"),
    path(
        "authors/",
        login_required(views.authors),
        name="authors",
    ),
    path(
        "authors/add/",
        login_required(views.author_add),
        name="author_add",
    ),
    path(
        "authors/<int:person_id>/",
        login_required(views.author_status),
        name="author_status",
    ),
    path("users/", login_required(views.users), name="users"),
    path(
        "users/add/",
        login_required(
            views.UserAddView.as_view(success_url=reverse_lazy("library:users"))
        ),
        name="user_add",
    ),
    path(
        "users/<int:person_id>/",
        login_required(views.user_status),
        name="user_status",
    ),
    path(
        "users/<int:person_id>/delete/",
        login_required(views.user_delete),
        name="user_delete",
    ),
    path("books/", login_required(views.books), name="books"),
    path(
        "books/add/",
        login_required(views.book_add),
        name="book_add",
    ),
    path(
        "books/<int:book_id>/",
        login_required(views.book_status),
        name="book_status",
    ),
    path(
        "books/<int:book_id>/delete/",
        login_required(views.book_delete),
        name="book_delete",
    ),
    path("rents/", login_required(views.rents), name="rents"),
    path(
        "rents/add/",
        login_required(
            views.RentAddView.as_view(success_url=reverse_lazy("library:rents"))
        ),
        name="rent_add",
    ),
    path(
        "rents/<int:rent_id>/",
        login_required(views.rent_status),
        name="rent_status",
    ),
    path(
        "rents/<int:rent_id>/return/",
        login_required(views.rent_return),
        name="rent_return",
    ),
]
