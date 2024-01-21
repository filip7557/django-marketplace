from django.urls import path
from marketplace.views import new


app_name = "marketplace"
urlpatterns = [
    path("new", new, name="new")
]