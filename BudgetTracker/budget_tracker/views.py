from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, UserProfile


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {"error": "incorrect credentials"}
            return render(request, "budget_tracker/login.html", context)
    else:
        return render(request, "budget_tracker/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password-confirm"]

        if password == password_confirm:
            try:
                User.objects.get(username=username)
                context = {"error": "username already taken"}
                return render(request, "budget_tracker/register.html", context)

            except User.DoesNotExist:
                User.objects.create_user(username, None, password)
                UserProfile.objects.create(
                    user=User.objects.get(username=username), savings=0.0
                )
                return redirect("/login/")
        else:
            context = {"username": username, "error": "passwords do not match"}
            return render(request, "budget_tracker/register.html", context)

    else:
        return render(request, "budget_tracker/register.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required(redirect_field_name="login_view", login_url="login/")
def index(request):
    set_savings(request)
    user_profile = User.objects.get(username=request.user.username).userprofile

    savings = user_profile.savings
    expense_list = Expense.objects.filter(userprofile=user_profile)
    income_list = Income.objects.filter(userprofile=user_profile)

    context = {
        "current_user": request.user,
        "savings": savings,
        "expenses": expense_list,
        "incomes": income_list,
    }
    return render(request, "budget_tracker/index.html", context)


def set_savings(request):
    user_profile = User.objects.get(username=request.user.username).userprofile
    expense_list = Expense.objects.filter(userprofile=user_profile)
    income_list = Income.objects.filter(userprofile=user_profile)

    user_profile.savings = 0

    if expense_list:
        for expense in expense_list:
            user_profile.savings -= expense.quantity

    if income_list:
        for income in income_list:
            user_profile.savings += income.quantity

    user_profile.savings = round(user_profile.savings, 2)

    user_profile.save()


@login_required(redirect_field_name="login_view", login_url="login/")
def add_expense(request):
    if request.method == "POST":
        expense_category = request.POST["category"]
        expense_quantity = float(request.POST["expense_quantity"])

        user_profile = User.objects.get(username=request.user.username).userprofile

        Expense.objects.create(
            category=expense_category,
            quantity=expense_quantity,
            userprofile=user_profile,
        )

        return redirect("/")
    else:
        return render(request, "budget_tracker/add_expense.html")


@login_required(redirect_field_name="login_view", login_url="login/")
def remove_expense(request, expense_id):
    expense_instance = Expense.objects.get(pk=expense_id)
    expense_instance.delete()

    return redirect("/")


@login_required(redirect_field_name="login_view", login_url="login/")
def edit_expense(request, expense_id):
    expense_instance = Expense.objects.get(pk=expense_id)

    if request.method == "POST":
        expense_category = request.POST["category"]
        expense_quantity = float(request.POST["expense_quantity"])

        expense_instance.quantity = expense_quantity
        expense_instance.category = expense_category
        expense_instance.save()

        return redirect("/")

    context = {"expense": expense_instance}
    return render(request, "budget_tracker/edit_expense.html", context)


@login_required(redirect_field_name="login_view", login_url="login/")
def add_income(request):
    if request.method == "POST":
        income_quantity = float(request.POST["income_quantity"])

        user_profile = User.objects.get(username=request.user.username).userprofile

        Income.objects.create(
            quantity=income_quantity,
            userprofile=user_profile,
        )

        return redirect("/")
    else:
        return render(request, "budget_tracker/add_income.html")


@login_required(redirect_field_name="login_view", login_url="login/")
def remove_income(request, income_id):
    income_instance = Income.objects.get(pk=income_id)
    income_instance.delete()

    return redirect("/")


@login_required(redirect_field_name="login_view", login_url="login/")
def edit_income(request, income_id):
    income_instance = Income.objects.get(pk=income_id)

    if request.method == "POST":
        income_quantity = float(request.POST["income_quantity"])

        income_instance.quantity = income_quantity
        income_instance.save()

        return redirect("/")

    context = {"income": income_instance}
    return render(request, "budget_tracker/edit_income.html", context)
