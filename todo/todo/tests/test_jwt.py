from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo.models import Todo


class JwtAuthenticationTests(APITestCase):
    def setUp(self):
        self.password = "Strong-test-password-902!"
        self.alice = User.objects.create_user(
            username="alice_jwt",
            password=self.password,
        )
        self.bob = User.objects.create_user(
            username="bob_jwt",
            password=self.password,
        )
        self.alice_todo = Todo.objects.create(
            title="Alice JWT todo",
            user=self.alice,
        )
        Todo.objects.create(
            title="Bob private JWT todo",
            user=self.bob,
        )

        self.token_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")
        self.verify_url = reverse("token_verify")
        self.todo_list_url = reverse("todo-api-list")

    def obtain_alice_tokens(self):
        """Log Alice in through the real JWT endpoint and return both tokens."""
        response = self.client.post(
            self.token_url,
            {
                "username": self.alice.username,
                "password": self.password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def use_bearer_token(self, token):
        """Send a token exactly as the future Next.js API client will send it."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_correct_credentials_return_access_and_refresh_tokens(self):
        tokens = self.obtain_alice_tokens()

        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)
        self.assertIsInstance(tokens["access"], str)
        self.assertIsInstance(tokens["refresh"], str)

    def test_wrong_password_returns_401(self):
        response = self.client.post(
            self.token_url,
            {
                "username": self.alice.username,
                "password": "incorrect-password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_access_token_can_call_todo_api(self):
        access_token = self.obtain_alice_tokens()["access"]
        self.use_bearer_token(access_token)

        response = self.client.get(self.todo_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.alice_todo.srno)

    def test_missing_token_returns_401(self):
        response = self.client.get(self.todo_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_returns_401(self):
        self.use_bearer_token("this-is-not-a-valid-jwt")

        response = self.client.get(self.todo_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_returns_new_access_token(self):
        refresh_token = self.obtain_alice_tokens()["refresh"]

        response = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIsInstance(response.data["access"], str)

    def test_refresh_token_cannot_access_todo_api(self):
        refresh_token = self.obtain_alice_tokens()["refresh"]
        self.use_bearer_token(refresh_token)

        response = self.client.get(self.todo_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_endpoint_accepts_valid_access_token(self):
        access_token = self.obtain_alice_tokens()["access"]

        response = self.client.post(
            self.verify_url,
            {"token": access_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_endpoint_rejects_invalid_token(self):
        response = self.client.post(
            self.verify_url,
            {"token": "this-is-not-a-valid-jwt"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_authenticated_alice_cannot_see_bob_todos(self):
        access_token = self.obtain_alice_tokens()["access"]
        self.use_bearer_token(access_token)

        response = self.client.get(self.todo_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_titles = [todo["title"] for todo in response.data]
        self.assertIn("Alice JWT todo", returned_titles)
        self.assertNotIn("Bob private JWT todo", returned_titles)
