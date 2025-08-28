from django.test import TestCase
from rest_framework.test import APIClient
from .models import CloudProvider

class ApiTest(TestCase):
    def test_cloud_provider_api(self):
        """
        Test the cloud provider API.
        """
        client = APIClient()
        response = client.get('/api/cloudproviders/')
        self.assertEqual(response.status_code, 200)

        CloudProvider.objects.create(name='Amazon Web Services', code='aws')
        response = client.get('/api/cloudproviders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Amazon Web Services')
