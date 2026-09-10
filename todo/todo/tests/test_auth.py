from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from todo.models import Todo


class TodoAuthorizationTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice",
            password="strong-test-password",
        )

        self.bob = User.objects.create_user(
            username="bob",
            password="strong-test-password",
        )

        self.alice_todo = Todo.objects.create(
            title="Alice's private todo",
            user=self.alice,
        )

    def test_user_cannot_edit_another_users_todo(self):
        self.client.login(
            username="bob",
            password="strong-test-password",
        )

        response = self.client.post(
            reverse(
                "edit_todo",
                args=[self.alice_todo.srno],
            ),
            {"title": "Changed by Bob"},
        )

        self.assertEqual(response.status_code, 404)

        self.alice_todo.refresh_from_db()

        self.assertEqual(
            self.alice_todo.title,
            "Alice's private todo",
        )