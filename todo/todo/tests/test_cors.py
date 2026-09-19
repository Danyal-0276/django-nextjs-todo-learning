from django.test import TestCase
from django.urls import reverse


class CorsTests(TestCase):
    def setUp(self):
        self.todo_url = reverse("todo-api-list")
        self.allowed_origin = "http://localhost:3000"
        self.blocked_origin = "https://malicious.example"

    def test_allowed_origin_preflight_succeeds(self):
        response = self.client.options(
            self.todo_url,
            headers={
                "origin": self.allowed_origin,
                "access-control-request-method": "GET",
                "access-control-request-headers": "authorization,content-type",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            self.allowed_origin,
        )

    def test_allowed_origin_receives_cors_header_on_unauthorized_response(self):
        response = self.client.get(
            self.todo_url,
            headers={
                "origin": self.allowed_origin,
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            self.allowed_origin,
        )

    def test_unknown_origin_is_not_allowed(self):
        response = self.client.options(
            self.todo_url,
            headers={
                "origin": self.blocked_origin,
                "access-control-request-method": "GET",
            },
        )

        self.assertIsNone(response.headers.get("Access-Control-Allow-Origin"))

    def test_html_login_page_does_not_receive_api_cors_header(self):
        response = self.client.get(
            reverse("login"),
            headers={
                "origin": self.allowed_origin,
            },
        )

        self.assertIsNone(response.headers.get("Access-Control-Allow-Origin"))
