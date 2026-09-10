from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from todo.models import Todo
from todo.forms import TodoForm

# Create your views here.


def signup(request):
    errors = {}

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        email = request.POST.get("email", "").strip()

        if not username:
            errors["username"] = "Username is required."
        if User.objects.filter(username=username).exists():
            errors["username"] = "Username already exists."

        try:
            validate_password(password, user=User(username=username, email=email))
        except ValidationError as e:
            errors["password"] = list(e.messages)

        if User.objects.filter(email=email).exists():
            errors["email"] = "An account already uses this email."

        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Please enter a valid email address."

        if not errors:
            User.objects.create_user(username=username, password=password, email=email)
            return redirect("login")

    return render(request, "signup.html", {"errors": errors})


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get(
            "username",
            "",
        ).strip()
        password = request.POST.get(
            "password",
            "",
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            auth_login(request, user)
            return redirect("todo-list")

        error = "Invalid username or password."

    return render(
        request,
        "loginn.html",
        {"error": error},
    )


@login_required(login_url="login")
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()

            return redirect("todo-list")
    else:
        form = TodoForm()

    res = Todo.objects.filter(
        user=request.user,
    ).order_by("-created_at")

    return render(
        request,
        "todo.html",
        {
            "res": res,
            "form": form,
        },
    )


@login_required(login_url="login")
def edit_todo(request, srno):
    obj = get_object_or_404(Todo, srno=srno, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("todo-list")
    else:
        form = TodoForm(instance=obj)
    return render(request, "edit_todo.html", {"obj": obj, "form": form})


@login_required(login_url="login")
@require_POST
def delete_todo(request, srno):
    obj = get_object_or_404(
        Todo,
        srno=srno,
        user=request.user,
    )

    obj.delete()

    return redirect("todo-list")


@login_required(login_url="login")
@require_POST
def signout(request):
    auth_logout(request)
    return redirect("login")


@login_required(login_url="login")
@require_POST
def toggle_todo(request, srno):
    obj = get_object_or_404(Todo, srno=srno, user=request.user)
    obj.completed = not obj.completed
    obj.save(update_fields=["completed", "updated_at"])
    return redirect("todo-list")
