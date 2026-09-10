from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from todo.models import Todo


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TodoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="Strong-test-password-902!")

    def test_todo_defaults_and_string_representation(self):
        todo = Todo.objects.create(title="Learn Django models", user=self.user)
        self.assertFalse(todo.completed)
        self.assertEqual(str(todo), "Learn Django models")
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)

    def test_updated_at_changes_when_todo_is_edited(self):
        todo = Todo.objects.create(title="Original", user=self.user)
        original_updated_at = todo.updated_at
        todo.title = "Updated"
        todo.save()
        todo.refresh_from_db()
        self.assertGreater(todo.updated_at, original_updated_at)

    def test_deleting_user_deletes_owned_todos(self):
        Todo.objects.create(title="Owned todo", user=self.user)
        self.user.delete()
        self.assertEqual(Todo.objects.count(), 0)
