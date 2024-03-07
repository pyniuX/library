from django.db import models

# from django.db.models import Deferrable, UniqueConstraint


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
    second_name = models.CharField(max_length=15, blank=True, null=True)
    surname = models.CharField(max_length=15)
    birth_date = models.DateField()
    death_date = models.DateField(blank=True, null=True)

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

    def __str__(self) -> str:
        return f"id:{self.id}, {self.title}"


class Rent(models.Model):
    """
    Rent class for borrowed books and things connected.
    """

    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        limit_choices_to={"is_active": True},
    )
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Book:{self.book.id} borrowed by user:{self.user.id}"
