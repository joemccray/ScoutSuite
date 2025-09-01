from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from scout_web.organizations.models import Organization, OrgRole
from scout_web.api.models import CloudProvider

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_login(self.user)

    # def test_list_agents(self):
    #     response = self.client.get('/api/agents/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json(), list)

    # def test_list_workflows(self):
    #     response = self.client.get('/api/workflows/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json(), list)

class OrganizationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('orguser', 'org@example.com', 'testpassword')
        self.organization = Organization.objects.create(name='Test Organization', slug='test-organization')
        self.org_role = OrgRole.objects.create(user=self.user, organization=self.organization, role=OrgRole.MEMBER)
        self.client.force_login(self.user)

    def test_create_cloud_provider(self):
        url = reverse('cloudprovider-list')
        data = {'name': 'Amazon Web Services', 'code': 'aws'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CloudProvider.objects.count(), 1)
        self.assertEqual(CloudProvider.objects.first().organization, self.organization)

    def test_list_cloud_providers(self):
        # Create a provider for the user's organization
        CloudProvider.objects.create(organization=self.organization, name='Amazon Web Services', code='aws')
        # Create a provider for another organization
        other_org = Organization.objects.create(name='Other Org', slug='other-org')
        CloudProvider.objects.create(organization=other_org, name='Google Cloud Platform', code='gcp')

        url = reverse('cloudprovider-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Amazon Web Services')
