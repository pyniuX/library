from django.contrib import admin
from django.db import models


class BookManager(models.Manager):
    """
    Class for Book class  connected custom queryset methods.
    """

    def status(self):
        """
        Returns if book is_available to rent for every book.
        """
        condition = models.Q(id__in=self.available())
        return self.annotate(is_available=condition)

    def available(self):
        """
        Returns all books that are 'on shelf' and can be borrowed.
        """
        return self.exclude(id__in=self.borrowed())

    def borrowed(self):
        """
        Returns all books that are borrowed and hadn't been returned.
        """
        return self.filter(rent__return_date__isnull=True, rent__book__isnull=False)


class RentQuerySet(models.QuerySet):
    """
    Class for Rent class connected custom queryset methods.
    """

    def for_books(self, *book_ids: int):
        """
        Returns rent history of book with given id.
        """
        return self.filter(book__in=book_ids)

    def for_users(self, *user_ids: int):
        """
        Returns rent history of user with given id.
        """
        return self.filter(user__in=user_ids)

    def by_closed(self):
        """
        Returns closed rents.
        """
        return self.by_return_date(False)

    def opened(self):
        """
        Returns open rents.
        """
        return self.by_return_date(True)

    def by_return_date(self, value: bool):
        """
        Help function returning open or close rents, depending on given value.
        """
        return self.filter(return_date__isnull=value)


class UserManager(models.Manager):
    """
    Class for User class connected custom queryset methods.
    """

    def status(self):
        """
        Returns account balance of every user.
        """
        return None


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

    objects = RentQuerySet().as_manager()

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


# DPME wyszukaj książkę: status książki z punktu widzenia użytkownika
# TODO: wyszukaj użytkownika z informacją: status wypożyczeń
# DONE książki w aktywnym wypożyczeniu,
# DONE książki dostępne do wypożyczenia
# DONE historia wypożyczeń użytkownika
# DONE historia wypożyczeń książki
# TODO: pokaz autorów i książki
