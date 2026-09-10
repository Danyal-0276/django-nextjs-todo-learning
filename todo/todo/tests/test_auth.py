from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class AuthenticationTests(TestCase):
    def setUp(self):
        self.password = "Strong-test-password-902!"
        self.user = User.objects.create_user(username="alice", email="alice@example.com", password=self.password)

    def test_signup_page_loads(self):
        self.assertEqual(self.client.get(reverse("signup")).status_code, 200)

    def test_valid_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse("signup"), {"username": "charlie", "email": "charlie@example.com", "password": "A-strong-password-731!"})
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="charlie", email="charlie@example.com").exists())

    def test_duplicate_username_is_rejected(self):
        response = self.client.post(reverse("signup"), {"username": "alice", "email": "other@example.com", "password": self.password})
        self.assertContains(response, "Username already exists.")
        self.assertEqual(User.objects.filter(username="alice").count(), 1)

    def test_duplicate_email_is_rejected(self):
        response = self.client.post(reverse("signup"), {"username": "other", "email": "alice@example.com", "password": self.password})
        self.assertContains(response, "An account already uses this email.")

    def test_invalid_email_is_rejected(self):
        response = self.client.post(reverse("signup"), {"username": "other", "email": "not-an-email", "password": self.password})
        self.assertContains(response, "Please enter a valid email address.")

    def test_weak_password_is_rejected(self):
        response = self.client.post(reverse("signup"), {"username": "other", "email": "other@example.com", "password": "123"})
        self.assertContains(response, "This password is too short.")
        self.assertFalse(User.objects.filter(username="other").exists())

    def test_valid_login_authenticates_user(self):
        response = self.client.post(reverse("login"), {"username": "alice", "password": self.password})
        self.assertRedirects(response, reverse("todo-list"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_invalid_login_displays_error(self):
        response = self.client.post(reverse("login"), {"username": "alice", "password": "wrong-password"})
        self.assertContains(response, "Invalid username or password.")

    def test_logout_requires_post_and_ends_session(self):
        self.client.login(username="alice", password=self.password)
        self.assertEqual(self.client.get(reverse("signout")).status_code, 405)
        response = self.client.post(reverse("signout"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
