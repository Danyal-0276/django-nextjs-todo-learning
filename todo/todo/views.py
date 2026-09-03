from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import Todo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method == "POST":
        # Handle signup logic here
        fnm = request.POST.get("fnm")
        lnm = request.POST.get("lnm")
        emailid = request.POST.get("email")
        pwd = request.POST.get("pwd")
        print(fnm, lnm, emailid, pwd)
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect("/loginn")

        pass
    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        fnm = request.POST.get("fnm")
        emailid = request.POST.get("email")
        pwd = request.POST.get("pwd")
        print(fnm, pwd)
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect("/todopage")
        else:
            return redirect("/loginn")
    return render(request, "loginn.html")

@login_required(login_url="/loginn")
def todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        obj = models.Todo(title=title, user=request.user)
        obj.save()
        res = models.Todo.objects.filter(user=request.user).order_by("-date")
        return render(request, "todo.html", {"res": res})
    res = models.Todo.objects.filter(user=request.user).order_by("-date")
    return render(request, "todo.html", {"res": res})

@login_required(login_url="/loginn")
def edit_todo(request, srno):
    if request.method == "POST":
        title = request.POST.get("title")
        obj = models.Todo.objects.get(srno=srno)
        obj.title = title
        obj.save()
        user = request.user
        return redirect("/todopage", {"obj": obj})
    obj = models.Todo.objects.get(srno=srno)
    return render(request, "todo.html", {"obj": obj})

@login_required(login_url="/loginn")
def delete_todo(request, srno):
    obj = models.Todo.objects.get(srno=srno)
    obj.delete()
    return redirect("/todopage")

@login_required(login_url="/loginn")
def signout(request):
    logout(request)
    return redirect("/loginn")
