from django.contrib import admin
from django.db.models import F

from .models import Book, Person, Rent

admin.site.register(Person)
admin.site.register(Book)
# admin.site.register(Rent)


class RentAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "borrow_date", "return_date"]
    ordering = [F("return_date").desc(nulls_first=True), "borrow_date"]
    list_filter = [
        "user",
        "book",
    ]


admin.site.register(Rent, RentAdmin)
