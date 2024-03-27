from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, ModelForm, PasswordInput, TextInput

from .models import Book, Person


class AuthorForm(ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "second_name",
            "surname",
            "birth_date",
            "death_date",
            "is_active",
        ]


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["authors", "title"]


class BookInAuthorForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title"]


class LoginForm(AuthenticationForm):
    username = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Input username",
            }
        ),
    )
    password = CharField(
        label="",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password",
            }
        ),
    )
