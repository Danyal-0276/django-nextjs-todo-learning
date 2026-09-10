from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from todo.models import Todo


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TodoViewTests(TestCase):
    def setUp(self):
        self.password = "Strong-test-password-902!"
        self.alice = User.objects.create_user(username="alice", password=self.password)
        self.bob = User.objects.create_user(username="bob", password=self.password)
        self.alice_todo = Todo.objects.create(title="Alice's private todo", user=self.alice)
        self.bob_todo = Todo.objects.create(title="Bob's private todo", user=self.bob)

    def login_as_alice(self):
        self.client.login(username="alice", password=self.password)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("todo-list"))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("todo-list")}')

    def test_user_sees_only_owned_todos(self):
        self.login_as_alice()
        response = self.client.get(reverse("todo-list"))
        visible_todos = list(response.context["res"])
        self.assertIn(self.alice_todo, visible_todos)
        self.assertNotIn(self.bob_todo, visible_todos)

    def test_user_can_create_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("todo-list"), {"title": "Learn Django forms"})
        self.assertRedirects(response, reverse("todo-list"))
        self.assertTrue(Todo.objects.filter(title="Learn Django forms", user=self.alice).exists())

    def test_blank_todo_is_rejected(self):
        self.login_as_alice()
        response = self.client.post(reverse("todo-list"), {"title": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todo title is required.")

    def test_user_can_edit_owned_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("edit_todo", args=[self.alice_todo.pk]), {"title": "Updated title"})
        self.assertRedirects(response, reverse("todo-list"))
        self.alice_todo.refresh_from_db()
        self.assertEqual(self.alice_todo.title, "Updated title")

    def test_user_cannot_edit_another_users_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("edit_todo", args=[self.bob_todo.pk]), {"title": "Not allowed"})
        self.assertEqual(response.status_code, 404)
        self.bob_todo.refresh_from_db()
        self.assertEqual(self.bob_todo.title, "Bob's private todo")

    def test_delete_requires_post(self):
        self.login_as_alice()
        self.assertEqual(self.client.get(reverse("delete_todo", args=[self.alice_todo.pk])).status_code, 405)
        self.assertTrue(Todo.objects.filter(pk=self.alice_todo.pk).exists())

    def test_user_can_delete_owned_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("delete_todo", args=[self.alice_todo.pk]))
        self.assertRedirects(response, reverse("todo-list"))
        self.assertFalse(Todo.objects.filter(pk=self.alice_todo.pk).exists())

    def test_user_cannot_delete_another_users_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("delete_todo", args=[self.bob_todo.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Todo.objects.filter(pk=self.bob_todo.pk).exists())

    def test_toggle_requires_post(self):
        self.login_as_alice()
        self.assertEqual(self.client.get(reverse("toggle_todo", args=[self.alice_todo.pk])).status_code, 405)

    def test_user_can_toggle_owned_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("toggle_todo", args=[self.alice_todo.pk]))
        self.assertRedirects(response, reverse("todo-list"))
        self.alice_todo.refresh_from_db()
        self.assertTrue(self.alice_todo.completed)

    def test_user_cannot_toggle_another_users_todo(self):
        self.login_as_alice()
        response = self.client.post(reverse("toggle_todo", args=[self.bob_todo.pk]))
        self.assertEqual(response.status_code, 404)
        self.bob_todo.refresh_from_db()
        self.assertFalse(self.bob_todo.completed)
