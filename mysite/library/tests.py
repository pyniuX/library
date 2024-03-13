from django.db import models
from django.test import TestCase

from .models import Book, IsActive, Person, Rent

# Create your tests here.


class IsActiveTests(TestCase):
    """
    Test for parental class IsActive from models.py
    """

    def setUP(self) -> None:
        self.list_objects = [
            IsActive(),
            IsActive(is_active=True),
            IsActive(is_active=False),
        ]
