from django.urls import path

from todo.legacy_ui import views


urlpatterns = [
    path("", views.signup, name="signup"),
    path("loginn/", views.login_view, name="login"),
    path("todopage/", views.todo, name="todo-list"),
    path("edit_todo/<int:srno>/", views.edit_todo, name="edit_todo"),
    path("delete_todo/<int:srno>/", views.delete_todo, name="delete_todo"),
    path("signout/", views.signout, name="signout"),
    path("toggle_todo/<int:srno>/", views.toggle_todo, name="toggle_todo"),
]
