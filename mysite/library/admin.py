from django.contrib import admin
from django.db.models import F

from .models import Book, Person, Rent

# admin.site.register(Person)
# admin.site.register(Book)
# admin.site.register(Rent)


class RentAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "borrow_date", "return_date"]
    ordering = [F("return_date").desc(nulls_first=True), "borrow_date"]
    list_filter = [
        "user",
        "book",
    ]


class OwnershipInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    inlines = [OwnershipInline]


class BookAdmin(admin.ModelAdmin):
    inlines = [OwnershipInline]
    exclude = ["authors"]


admin.site.register(Rent, RentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Person, PersonAdmin)
