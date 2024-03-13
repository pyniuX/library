import datetime

from django.db import models


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

    class PersonQuerySet(models.QuerySet):
        """
        Class for User class connected custom queryset methods.
        """

        def active(self):
            """
            Returns persons with is_active true: active library users and author-users.
            """
            return self.filter(is_active=True)

        def authors(self):
            """
            Returns authors (persons with at least one written book).
            """
            ids = [self.filter(book__authors__isnull=False).distinct().values("id")]
            return self.filter(id__in=ids)

        def count_rents(self, count_filter=None):
            """
            Returns number of all rents for user, depending on a filter..
            """
            return self.annotate(
                book_count=models.Count("rent__book", filter=count_filter)
            )

        def count_closed_rents(self):
            """
            Returns number of closed rents for user in book_count field.
            """
            return self.count_rents(
                count_filter=models.Q(rent__in=Rent.objects.closed())
            )

        def count_opened_rents(self):
            """
            Returns number of ongoing rents for user in book_count field.
            """
            return self.count_rents(
                count_filter=models.Q(rent__in=Rent.objects.opened())
            )

        def inactive(self):
            """
            Returns persons with is_active false: non-user authors, and former users.
            """
            return self.filter(is_active=False)

        def users(self):
            """
            Returns users (persons with at least one borrowed book).
            """
            ids = [self.filter(rent__user__isnull=False).distinct().values("id")]
            return self.filter(id__in=ids)

    objects = PersonQuerySet().as_manager()

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Book(IsActive):
    """
    Book class for all books.
    """

    authors = models.ManyToManyField(Person)
    title = models.CharField(max_length=512)

    class BookQuerySet(models.QuerySet):
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

    objects = BookQuerySet().as_manager()

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

    class RentQuerySet(models.QuerySet):
        """
        Class for Rent class connected custom queryset methods.
        """

        def _by_return_date(self, value: bool):
            """
            Help function returning open or close rents, depending on given value.
            """
            return self.filter(return_date__isnull=value)

        def closed(self):
            """
            Returns closed rents.
            """
            return self._by_return_date(False)

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

        # def since(self, date: datetime.date):
        #     """
        #     Returns rents greater than or equal to given date..
        #     """
        #     return self.filter()

        def opened(self):
            """
            Returns open rents.
            """
            return self._by_return_date(True)

    objects = RentQuerySet().as_manager()

    def __str__(self) -> str:
        return f"Book:{self.book_id} borrowed by user:{self.user_id}"


# DONE wyszukaj książkę: status książki z punktu widzenia użytkownika
# DONE wyszukaj użytkownika z informacją: status wypożyczeń
# DONE książki w aktywnym wypożyczeniu,
# DONE książki dostępne do wypożyczenia
# DONE historia wypożyczeń użytkownika
# DONE historia wypożyczeń książki
# TODO: pokaz autorów i książki
# TODO: wypożyczenia z okresy
