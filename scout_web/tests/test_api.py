from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_login(self.user)

    def test_list_agents(self):
        response = self.client.get('/api/agents/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_list_workflows(self):
        response = self.client.get('/api/workflows/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
