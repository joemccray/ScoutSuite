from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from .models import CloudProvider, Account, Scan, Finding

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.provider = CloudProvider.objects.create(name='Amazon Web Services', code='aws')
        self.account = Account.objects.create(
            provider=self.provider,
            name='Test Account',
            credentials={'aws_access_key_id': 'test', 'aws_secret_access_key': 'test'}
        )

    def test_cloud_provider_api(self):
        """
        Test the cloud provider API.
        """
        response = self.client.get('/api/cloudproviders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Amazon Web Services')

    @patch('api.tasks.run_scan.delay')
    def test_scan_api_endpoint(self, mock_run_scan_delay):
        """
        Test the scan API endpoint.
        """
        response = self.client.post(f'/api/accounts/{self.account.id}/scan/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'scan_started')

        # Check that a Scan object was created
        self.assertEqual(Scan.objects.count(), 1)
        scan = Scan.objects.first()
        self.assertEqual(scan.account, self.account)
        self.assertEqual(scan.status, 'PENDING')

        # Check that the Celery task was called
        mock_run_scan_delay.assert_called_once_with(scan.id)

    @patch('api.tasks.run_from_api')
    def test_run_scan_task_success(self, mock_run_from_api):
        """
        Test the run_scan Celery task in a success scenario.
        """
        # Mock the return value of run_from_api
        class MockCloudProvider:
            findings = {
                'finding-1': {'rule_name': 'test-rule-1', 'description': 'Test description 1', 'level': 'high'}
            }
        mock_run_from_api.return_value = MockCloudProvider()

        # Create a scan to run
        scan = Scan.objects.create(account=self.account, status='PENDING')

        # Run the task
        from .tasks import run_scan
        run_scan(scan.id)

        # Refresh the scan object from the database
        scan.refresh_from_db()

        # Assert that the scan is marked as completed
        self.assertEqual(scan.status, 'COMPLETED')
        self.assertIsNotNone(scan.completed_at)

        # Assert that findings were created
        self.assertEqual(Finding.objects.count(), 1)
        finding = Finding.objects.first()
        self.assertEqual(finding.scan, scan)
        self.assertEqual(finding.rule_name, 'test-rule-1')

    @patch('api.tasks.run_from_api')
    def test_run_scan_task_failure(self, mock_run_from_api):
        """
        Test the run_scan Celery task in a failure scenario.
        """
        # Mock run_from_api to raise an exception
        mock_run_from_api.side_effect = Exception("Scan failed")

        # Create a scan to run
        scan = Scan.objects.create(account=self.account, status='PENDING')

        # Run the task and expect an exception
        from .tasks import run_scan
        with self.assertRaises(Exception):
            run_scan(scan.id)

        # Refresh the scan object from the database
        scan.refresh_from_db()

        # Assert that the scan is marked as failed
        self.assertEqual(scan.status, 'FAILED')
        self.assertIsNotNone(scan.completed_at)

        # Assert that no findings were created
        self.assertEqual(Finding.objects.count(), 0)
