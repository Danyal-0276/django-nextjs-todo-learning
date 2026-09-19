from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegistrationApiTests(APITestCase):
    def setUp(self):
        self.registration_url = reverse("register")