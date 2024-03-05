from django.http import HttpResponse
from django.shortcuts import render

from .models import Person


def index(request):
    return render(request, "library/index.html")
