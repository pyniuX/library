from django.urls import path
from library import views

app_name = "library"
urlpatterns = [
    path("", views.index, name="index"),
    path("people", views.people, name="people"),
    path("people/authors", views.authors, name="authors"),
    path("people/users", views.users, name="users"),
    path("books", views.books, name="books"),
    path("rents", views.rents, name="rents"),
]
