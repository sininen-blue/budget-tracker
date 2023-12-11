from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Expense, Income


def index(request):
    set_savings()
    savings = User.objects.get(username="neil").userprofile.savings
    context = {
        "savings": savings,
        "expenses": Expense.objects.all(),
        "incomes": Income.objects.all(),
    }
    return render(request, "budget_tracker/index.html", context)


def set_savings():
    expense_list = Expense.objects.all()
    income_list = Income.objects.all()

    user_profile = User.objects.get(username="neil").userprofile
    user_profile.savings = 0

    if expense_list:
        for expense in expense_list:
            user_profile.savings -= expense.quantity

    if income_list:
        for income in income_list:
            user_profile.savings += income.quantity

    user_profile.save()


def add_expense(request):
    if request.method == "POST":
        expense_category = request.POST["category"]
        expense_quantity = float(request.POST["expense_quantity"])
        Expense.objects.create(category=expense_category, quantity=expense_quantity)

        return redirect("/")
    else:
        return render(request, "budget_tracker/add_expense.html")


def remove_expense(request, expense_id):
    expense_instance = Expense.objects.get(pk=expense_id)
    expense_instance.delete()

    return redirect("/")


def edit_expense(request, expense_id):
    expense_instance = Expense.objects.get(pk=expense_id)

    if request.method == "POST":
        expense_category = request.POST["category"]
        expense_quantity = float(request.POST["expense_quantity"])

        expense_instance.quantity = expense_quantity
        expense_instance.category = expense_category
        expense_instance.save()

        return redirect("/")

    context = {
        "expense": expense_instance
    }
    return render(request, "budget_tracker/edit_expense.html", context)


def add_income(request):
    if request.method == "POST":
        income_quantity = float(request.POST["income_quantity"])
        Income.objects.create(quantity=income_quantity)

        current_user = User.objects.get(username="neil")
        current_user.userprofile.savings += income_quantity
        current_user.userprofile.save()

        print(current_user.userprofile.savings)

        return redirect("/")
    else:
        return render(request, "budget_tracker/add_income.html")


def remove_income(request, income_id):
    income_instance = Income.objects.get(pk=income_id)
    income_instance.delete()

    return redirect("/")


def edit_income(request, income_id):
    income_instance = Income.objects.get(pk=income_id)

    if request.method == "POST":
        income_quantity = float(request.POST["income_quantity"])

        income_instance.quantity = income_quantity
        income_instance.save()

        return redirect("/")

    context = {
        "income": income_instance
    }
    return render(request, "budget_tracker/edit_income.html", context)
