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

from todo.models import Todo

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
            validate_password(password)
        except ValidationError as e:
            errors["password"] = list(e.messages)

        if not errors:
            User.objects.create_user(username=username, password=password, email=email)
            return redirect("/loginn")
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


@login_required(login_url="/loginn/")
def todo(request):
    error = None

    if request.method == "POST":
        title = request.POST.get("title", "").strip()

        if not title:
            error = "Todo title is required."
        else:
            Todo.objects.create(
                title=title,
                user=request.user,
            )
            return redirect("todo-list")

    res = Todo.objects.filter(
        user=request.user,
    ).order_by("-date")

    return render(
        request,
        "todo.html",
        {
            "res": res,
            "error": error,
        },
    )


@login_required(login_url="/loginn")
def edit_todo(request, srno):
    obj = get_object_or_404(Todo, srno=srno, user=request.user)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if not title:
            return render(
                request,
                "edit_todo.html",
                {"obj": obj, "error": "Title cannot be empty."},
            )
        obj.title = title
        obj.save()
        return redirect("/todopage/")
    return render(request, "edit_todo.html", {"obj": obj})


@login_required(login_url="/loginn/")
@require_POST
def delete_todo(request, srno):
    obj = get_object_or_404(
        Todo,
        srno=srno,
        user=request.user,
    )

    obj.delete()

    return redirect("/todopage/")


@login_required(login_url="/loginn/")
def signout(request):
    auth_logout(request)
    return redirect("login")
