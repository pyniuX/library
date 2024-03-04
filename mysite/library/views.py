from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic

from .models import Person


class IndexView(generic.ListView):
    template_name = "library/index.html"
    context_object_name = "main menu"
