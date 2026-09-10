from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo.models import Todo


class TodoApiTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice_api",
            password="Strong-test-password-902!",
        )

        self.bob = User.objects.create_user(
            username="bob_api",
            password="Strong-test-password-902!",
        )

        self.alice_todo = Todo.objects.create(
            title="Alice API todo",
            user=self.alice,
        )

        self.bob_todo = Todo.objects.create(
            title="Bob API todo",
            user=self.bob,
        )

        self.list_url = reverse("todo-api-list")

    def detail_url(self, todo):
        return reverse("todo-api-detail", args=[todo.srno])

    def test_unauthenticated_user_cannot_access_todos(self):
        response = self.client.get(self.list_url)

        # Session authentication returns 403, while JWT will normally return 401.
        # Either response means an anonymous user was correctly denied access.
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_alice_can_only_list_alice_todos(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.alice_todo.srno)
        self.assertEqual(response.data[0]["title"], "Alice API todo")

    def test_bob_can_only_list_bob_todos(self):
        self.client.force_authenticate(user=self.bob)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.bob_todo.srno)
        self.assertEqual(response.data[0]["title"], "Bob API todo")

    def test_create_todo_assigns_authenticated_user(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.post(
            self.list_url,
            {"title": "Created through API", "completed": False},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_todo = Todo.objects.get(srno=response.data["id"])
        self.assertEqual(created_todo.user, self.alice)
        self.assertEqual(created_todo.title, "Created through API")

    def test_alice_can_retrieve_her_own_todo(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.get(self.detail_url(self.alice_todo))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.alice_todo.srno)
        self.assertEqual(response.data["title"], "Alice API todo")

    def test_alice_cannot_retrieve_bob_todo(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.get(self.detail_url(self.bob_todo))

        # The user-filtered queryset hides the object instead of revealing that
        # another user's todo exists.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_alice_can_update_her_own_todo(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.patch(
            self.detail_url(self.alice_todo),
            {"title": "Alice updated todo", "completed": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.alice_todo.refresh_from_db()
        self.assertEqual(self.alice_todo.title, "Alice updated todo")
        self.assertTrue(self.alice_todo.completed)

    def test_alice_cannot_update_bob_todo(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.patch(
            self.detail_url(self.bob_todo),
            {"title": "Changed by Alice"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.bob_todo.refresh_from_db()
        self.assertEqual(self.bob_todo.title, "Bob API todo")

    def test_alice_can_delete_her_own_todo(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.delete(self.detail_url(self.alice_todo))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(srno=self.alice_todo.srno).exists())

    def test_alice_cannot_delete_bob_todo(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.delete(self.detail_url(self.bob_todo))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Todo.objects.filter(srno=self.bob_todo.srno).exists())

    def test_blank_title_is_rejected(self):
        self.client.force_authenticate(user=self.alice)

        response = self.client.post(
            self.list_url,
            {"title": "", "completed": False},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertEqual(Todo.objects.filter(user=self.alice).count(), 1)

    def test_generated_fields_cannot_be_set_manually(self):
        self.client.force_authenticate(user=self.alice)
        supplied_timestamp = "2000-01-01T00:00:00Z"

        response = self.client.post(
            self.list_url,
            {
                "id": 999999,
                "title": "Todo with attempted generated fields",
                "completed": False,
                "created_at": supplied_timestamp,
                "updated_at": supplied_timestamp,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_todo = Todo.objects.get(title="Todo with attempted generated fields")
        self.assertNotEqual(created_todo.srno, 999999)
        self.assertNotEqual(created_todo.created_at.year, 2000)
        self.assertNotEqual(created_todo.updated_at.year, 2000)
