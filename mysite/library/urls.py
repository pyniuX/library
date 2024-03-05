from django.urls import path
from library.views import index

app_name = "library"
urlpatterns = [path("", index, name="index")]
