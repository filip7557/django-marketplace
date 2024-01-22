from django.urls import path
from marketplace.views import new, buy


app_name = "marketplace"
urlpatterns = [
    path("new", new, name="new"),
    path("buy", buy, name="buy"),
]