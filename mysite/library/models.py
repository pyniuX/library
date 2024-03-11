from django.contrib import admin
from django.db import models


class BookManager(models.Manager):
    """
    Class for custom queryset methods.
    """

    def book_status(self):

        condition = models.Q(id__in=self.filter_available())
        return self.annotate(is_available=condition)

    def filter_borrowed(self):
        return self.filter(
            rent__return_date__isnull=True, rent__borrow_date__isnull=False
        )

    def filter_available(self):
        borrowed = self.filter_borrowed()
        return self.exclude(id__in=borrowed)


class IsActive(models.Model):
    """
    Parent class containing is_active bracket
    for books existing in library and library users.
    """

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Person(IsActive):
    """
    Person class for future users and book authors.
    """

    name = models.CharField(max_length=15)
    second_name = models.CharField(
        max_length=15,
        default="",
        blank=True,
    )
    surname = models.CharField(max_length=15)
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "surname", "birth_date"],
                name="unique_person",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Book(IsActive):
    """
    Book class for all books.
    """

    authors = models.ManyToManyField(Person)
    title = models.CharField(max_length=512)

    objects = BookManager()

    def __str__(self) -> str:
        return f"[id:{self.id}] {self.title} "


class Rent(models.Model):
    """
    Rent class for borrowed books and things connected.
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        limit_choices_to={"is_active": True},
    )
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book"],
                condition=models.Q(return_date__isnull=True),
                name="unique_book_rent",
            )
        ]

    def __str__(self) -> str:
        return f"Book:{self.book_id} borrowed by user:{self.user_id}"


# TODO: wyszukaj książkę: status książki z punktu widzenia użytkownika
# TODO: wyszukaj użytkownika z informacją: status wypożyczeń
# TODO książki w aktywnym wypożyczeniu,
# TODO książki dostępne do wypożyczenia
# TODO: historia wypożyczeń użytkownika
# TODO: historia wypożyczeń książki
# TODO: pokaz autorów i książki
