from datetime import date

from django.db import models


class Person(models.Model):
    """Person class for library users and book authors."""

    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    birth_date = models.DateField()
    death_date = models.DateField(default=None)
