from django.contrib import admin

from .models import Book, Person, Rent

admin.site.register(Person)
admin.site.register(Book)
admin.site.register(Rent)
