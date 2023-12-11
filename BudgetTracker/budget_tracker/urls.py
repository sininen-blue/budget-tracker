from django.urls import path
from . import views

app_name = "budget_tracker"
urlpatterns = [
    path("", views.index, name="index"),
    path("expense/add/", views.add_expense, name="add_expense"),
    path("expense/<int:expense_id>/remove/", views.remove_expense, name="remove_expense"),
    path("expense/<int:expense_id>/edit/", views.edit_expense, name="edit_expense"),

    path("income/add/", views.add_income, name="add_income"),
    path("income/<int:income_id>/remove/", views.remove_income, name="remove_income"),
    path("income/<int:income_id>/edit/", views.edit_income, name="edit_income"),

    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("register/", views.register_view, name="register_view"),
]
