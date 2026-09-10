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