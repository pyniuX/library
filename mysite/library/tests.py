import datetime

from django.db import models
from django.test import TestCase

from .models import Book, IsActive, Person, Rent

# Create your tests here.


class SetUpTestData(TestCase):
    """
    Parent class containing method for setting up test data
    """

    @classmethod
    def setup_database(cls) -> None:
        cls.list_persons = [
            # only users
            # list_index = 0, db_id =  1
            Person(
                name="Adam",
                surname="Wąsek",
                birth_date=datetime.date(1996, 6, 12),
            ),
            # list_index = 1, db_id =  2
            Person(
                name="Piotr",
                surname="Adamczyk",
                birth_date=datetime.date(1988, 5, 1),
                is_active=True,
            ),
            # list_index = 2, db_id =  3
            Person(
                name="Anna",
                second_name="Katarzyna",
                surname="Lewandowska",
                birth_date=datetime.date(2000, 1, 1),
            ),
            # list_index = 3, db_id =  4
            Person(
                name="Hanna",
                second_name="Weronika",
                surname="Łęcka",
                birth_date=datetime.date(1965, 2, 5),
                is_active=True,
            ),
            # users and authors
            # list_index = 4, db_id =  5
            Person(
                name="Olga",
                second_name="Nawoja",
                surname="Tokarczuk",
                birth_date=datetime.date(1962, 1, 29),
            ),
            # list_index = 5, db_id =  6
            Person(
                name="Remigiusz",
                surname="Mróz",
                birth_date=datetime.date(1987, 1, 15),
            ),
            # only authors
            # list_index = 6, db_id =  7
            Person(
                name="Adam",
                second_name="Bernard",
                surname="Mickiewicz",
                birth_date=datetime.date(1798, 12, 13),
                death_date=datetime.date(1855, 11, 26),
                is_active=False,
            ),
            # list_index = 7, db_id =  8
            Person(
                name="Zofia",
                surname="Nałkowska",
                birth_date=datetime.date(1884, 11, 10),
                death_date=datetime.date(1954, 12, 17),
                is_active=False,
            ),
        ]

        cls.list_books = [
            # list_index = 0, db_id =  1
            Book(title="Bieguni"),
            # list_index = 1, db_id =  2
            Book(title="Uprowadzenie"),
            # list_index = 2, db_id =  3
            Book(title="Pan Tadeusz"),
            # list_index = 3, db_id =  4
            Book(title="Nad Niemnem"),
            # list_index = 4, db_id =  5
        ]

        cls.db_ids = {
            "users_only": [1, 2, 3, 4],
            "users_and_authors": [5, 6],
            "authors_only": [7, 8],
            "users_with_open_rents": [3, 5],
            "users_with_closed_rents": [1, 3, 5],
            "rents_number": [1, 0, 2, 0, 2, 0, 0, 0],
            "borrowed_books": [1, 2],
        }
        for e in cls.list_persons:
            e.save()
        licznik = len(cls.db_ids["users_only"]) + 1
        for e in cls.list_books:
            e.save()
            e.authors.add(Person.objects.get(id=licznik))
            licznik += 1

        cls.list_rents = [
            # ended rents
            # list_index = 0, db_id =  1
            Rent(
                book=Book.objects.get(id=1),
                user=Person.objects.get(id=1),
                borrow_date=datetime.date(2023, 10, 4),
                return_date=datetime.date(2023, 11, 6),
            ),
            # list_index = 1, db_id =  2
            Rent(
                book=Book.objects.get(id=1),
                user=Person.objects.get(id=5),
                borrow_date=datetime.date(2024, 1, 4),
                return_date=datetime.date(2024, 2, 2),
            ),
            # list_index = 2, db_id =  3
            Rent(
                book=Book.objects.get(id=2),
                user=Person.objects.get(id=3),
                borrow_date=datetime.date(2024, 1, 18),
                return_date=datetime.date(2024, 2, 6),
            ),
            # ongoing rents
            # list_index = 3, db_id =  4
            Rent(
                book=Book.objects.get(id=1),
                user=Person.objects.get(id=3),
                borrow_date=datetime.date(2024, 3, 12),
            ),
            # list_index = 4, db_id =  5
            Rent(
                book=Book.objects.get(id=2),
                user=Person.objects.get(id=5),
                borrow_date=datetime.date(2024, 3, 1),
            ),
        ]
        for e in cls.list_rents:
            e.save()

    class Meta:
        abstract = True


class PersonClassTests(SetUpTestData):
    """
    Test for Person class form models.py
    """

    @classmethod
    def setUpTestData(self) -> None:
        SetUpTestData.setup_database()

    def test_qs_active_should_yield_plain_qs(self):
        """
        is_active() should result in plain qs,
        given data: authors_only and one undeclared field
        """
        with self.subTest():
            self.assertEqual(
                Person.objects.filter(id__in=self.db_ids["authors_only"])
                .active()
                .count(),
                0,
            )
        self.assertEqual(
            Person.objects.filter(id=len(self.list_persons) + 1).active().count(), 0
        )

    def test_qs_active_should_yield_all_active(self):
        """
        is_active() should result in all persons from database, where is_active = True
        given data: all persons
        """
        self.assertQuerySetEqual(
            Person.objects.active(),
            Person.objects.exclude(id__in=self.db_ids["authors_only"]),
            ordered=False,
        )

    def test_qs_active_should_yield_all_active_from_users(self):
        """
        is_active() should result in all users
        given data: users_only
        """
        self.assertQuerySetEqual(
            Person.objects.filter(id__in=self.db_ids["users_only"]).active(),
            Person.objects.filter(id__in=self.db_ids["users_only"]),
            ordered=False,
        )

    def test_qs_authors_should_yield_plain_qs(self):
        """
        authors() should result in plain qs
        given data: users_only and one undeclared field
        """
        with self.subTest():
            self.assertEqual(
                Person.objects.filter(id__in=self.db_ids["users_only"])
                .authors()
                .count(),
                0,
            )
        self.assertEqual(Person.objects.filter(id=0).authors().count(), 0)

    def test_qs_authors_should_yield_all_authors(self):
        """
        authors() should result in all authors from database, who have at least one book in Book class
        given data: all persons
        """
        self.assertQuerySetEqual(
            Person.objects.authors(),
            Person.objects.filter(
                id__in=self.db_ids["authors_only"] + self.db_ids["users_and_authors"],
            ),
            ordered=False,
        )

    def test_qs_authors_should_yield_all_authors_from_authors(self):
        """
        authors() should result in all authors
        given data: authors_only and users_and_authors
        """
        self.assertQuerySetEqual(
            Person.objects.filter(
                id__in=self.db_ids["authors_only"] + self.db_ids["users_and_authors"]
            ).authors(),
            Person.objects.filter(
                id__in=self.db_ids["authors_only"] + self.db_ids["users_and_authors"]
            ),
            ordered=False,
        )

    def test_qs_annotate_rents_number_should_yield_zero(self):
        """
        .annotate_rents_number() should result in annotated rents_count fields with value 0
        given data: users without any rents
        """
        ids_with_any_rents = list(
            set(
                self.db_ids["users_with_closed_rents"]
                + self.db_ids["users_with_open_rents"]
            )
        )
        ids_without_any_rents = [i for i in range(1, 9) if i not in ids_with_any_rents]
        for e in Person.objects.filter(
            id__in=ids_without_any_rents
        ).annotate_rents_number():
            with self.subTest():
                self.assertEqual(e.rents_count, 0)

    def test_qs_annotate_rents_number_should_yield_appropriate_values(self):
        """
        .annotate_rents_number() should result in annotated rents_count fields with values from self.db[count_rents]
        given data: all persons
        """
        licznik = 0
        for e in Person.objects.order_by("id").annotate_rents_number():
            with self.subTest():
                self.assertEqual(e.rents_count, self.db_ids["rents_number"][licznik])
            licznik += 1

    def test_qs_annotate_rents_number_should_yield_appropriate_values_2(self):
        """
        .annotate_rents_number() should result in annotated rents_count fields with values from self.db[count_rents]
        given data: persons with at least one rent
        """
        ids_with_any_rents = list(
            set(
                self.db_ids["users_with_closed_rents"]
                + self.db_ids["users_with_open_rents"]
            )
        )
        licznik = 0
        for e in (
            Person.objects.filter(id__in=ids_with_any_rents)
            .order_by("id")
            .annotate_rents_number()
        ):
            with self.subTest():
                self.assertEqual(
                    e.rents_count,
                    self.db_ids["rents_number"][ids_with_any_rents[licznik] - 1],
                )
            licznik += 1

    def test_qs_inactive(self):
        """
        .inactive() should result in all persons with is_active = False
        given data: all persons
        """
        self.assertQuerySetEqual(
            Person.objects.inactive(),
            Person.objects.filter(id__in=self.db_ids["authors_only"]),
            ordered=False,
        )


class BookClassTests(SetUpTestData):

    @classmethod
    def setUpTestData(self) -> None:
        SetUpTestData.setup_database()

    def test_qs_borrowed_returns_plain_qs(self):
        """
        .borrowed() should result in plaint qs
        given data: all books that are not actively borrowed and one plain field
        """
        not_borrowed_books = [
            e
            for e in range(1, Book.objects.count() + 1)
            if e not in self.db_ids["borrowed_books"]
        ]
        self.assertEqual(
            Book.objects.filter(id__in=not_borrowed_books).borrowed().count(), 0
        )

    def test_qs_borrowed_returns_all_borrowed_books(self):
        """
        .borrowed() should result in all actively borrowed books
        given data: all books
        """
        self.assertQuerySetEqual(
            Book.objects.borrowed(),
            Book.objects.filter(id__in=self.db_ids["borrowed_books"]),
            ordered=False,
        )

    def test_qs_borrowed_returns_all_borrowed_books_from_borrowed_books(self):
        """
        .borrowed() should result in all actively borrowed books
        given data: actively borrowed books
        """
        self.assertQuerySetEqual(
            Book.objects.filter(id__in=self.db_ids["borrowed_books"]).borrowed(),
            Book.objects.filter(id__in=self.db_ids["borrowed_books"]),
            ordered=False,
        )

    def test_qs_available_returns_plain_qs(self):
        """
        .available() should result in plaint qs
        given data: all books that are  actively borrowed
        """

        self.assertEqual(
            Book.objects.filter(id__in=self.db_ids["borrowed_books"])
            .available()
            .count(),
            0,
        )

    def test_qs_available_returns_all_available_books(self):
        """
        .available() should result in all books available to borrow
        given data: all books
        """
        self.assertQuerySetEqual(
            Book.objects.available(),
            Book.objects.exclude(id__in=self.db_ids["borrowed_books"]),
            ordered=False,
        )

    def test_qs_available_returns_all_available_books_from_available_books(self):
        """
        .available() should result in all books available to borrow
        given data: available books
        """
        self.assertQuerySetEqual(
            Book.objects.exclude(id__in=self.db_ids["borrowed_books"]).available(),
            Book.objects.exclude(id__in=self.db_ids["borrowed_books"]),
            ordered=False,
        )


# TODO: create books, because authors() method is not working without it
