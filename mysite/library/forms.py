from django.forms import BaseInlineFormSet, ModelForm

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
