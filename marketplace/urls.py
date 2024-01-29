from django.urls import path
from marketplace.views import register, profile, solve_dispute, disputes, new, buy


app_name = "marketplace"
urlpatterns = [
    path("new", new, name="new"),
    path("buy", buy, name="buy"),
    path("disputes", disputes, name="disputes"),
    path("solve_dispute", solve_dispute, name="solve_dispute"),
    path("profile/<int:user_id>/", profile, name="profile"),
    path("register", register, name="register")
]