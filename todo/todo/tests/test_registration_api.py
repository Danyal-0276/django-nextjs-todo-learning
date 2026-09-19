from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationApiTests(APITestCase):
    def setUp(self):
        self.registration_url = reverse("register")
        self.valid_payload = {
            "username": "new_api_user",
            "email": "new_api_user@example.com",
            "password": "Strong-test-password-902!",
            "password_confirm": "Strong-test-password-902!",
        }

    def register(self, **overrides):
        payload = {**self.valid_payload, **overrides}
        return self.client.post(
            self.registration_url,
            payload,
            format="json",
        )

    def test_anonymous_user_can_register(self):
        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_registration_creates_user(self):
        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(
                username=self.valid_payload["username"],
                email=self.valid_payload["email"],
            ).exists()
        )

    def test_registered_password_is_hashed(self):
        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=self.valid_payload["username"])
        self.assertNotEqual(user.password, self.valid_payload["password"])
        self.assertTrue(user.check_password(self.valid_payload["password"]))

    def test_password_fields_are_not_returned(self):
        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertNotIn("password_confirm", response.data)

    def test_mismatched_passwords_are_rejected(self):
        response = self.register(password_confirm="Different-password-903!")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", response.data)
        self.assertFalse(
            User.objects.filter(username=self.valid_payload["username"]).exists()
        )

    def test_weak_password_is_rejected(self):
        response = self.register(
            password="password",
            password_confirm="password",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_entirely_numeric_password_is_rejected(self):
        response = self.register(
            password="12345678",
            password_confirm="12345678",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(
            username=self.valid_payload["username"],
            email="existing-username@example.com",
            password="Existing-test-password-902!",
        )

        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_duplicate_email_is_rejected_case_insensitively(self):
        User.objects.create_user(
            username="existing_email_user",
            email="NEW_API_USER@example.com",
            password="Existing-test-password-902!",
        )

        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertFalse(
            User.objects.filter(username=self.valid_payload["username"]).exists()
        )

    def test_invalid_email_is_rejected(self):
        response = self.register(email="not-an-email")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_required_fields_are_enforced(self):
        for missing_field in ["username", "email", "password", "password_confirm"]:
            with self.subTest(missing_field=missing_field):
                payload = self.valid_payload.copy()
                payload.pop(missing_field)

                response = self.client.post(
                    self.registration_url,
                    payload,
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )
                self.assertIn(missing_field, response.data)

    def test_registered_user_can_obtain_jwt_tokens(self):
        registration_response = self.register()
        self.assertEqual(
            registration_response.status_code,
            status.HTTP_201_CREATED,
        )

        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": self.valid_payload["username"],
                "password": self.valid_payload["password"],
            },
            format="json",
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)
