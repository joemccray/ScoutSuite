from django.test import TestCase
from unittest.mock import patch, MagicMock
from scout_web.api.models import CloudProvider, Account, Scan, Finding
from scout_web.api.services import ScanService
import datetime

class ScanServiceTest(TestCase):
    def setUp(self):
        self.provider = CloudProvider.objects.create(name='AWS', code='aws')
        self.account = Account.objects.create(name='Test Account', provider=self.provider, credentials={'aws_access_key_id': 'test', 'aws_secret_access_key': 'test'})
        self.scan = Scan.objects.create(account=self.account, status='PENDING', configuration={})

    @patch('scout_web.api.services.run_from_api')
    def test_run_scan_success(self, mock_run_from_api):
        # Mock the return value of the ScoutSuite API
        mock_findings = {
            'finding-1': {'rule_name': 'Test Rule 1', 'description': 'Test Description 1', 'level': 'danger'},
            'finding-2': {'rule_name': 'Test Rule 2', 'description': 'Test Description 2', 'level': 'warning'},
        }
        mock_cloud_provider = MagicMock()
        mock_cloud_provider.findings = mock_findings
        mock_run_from_api.return_value = mock_cloud_provider

        # Call the service
        result = ScanService.run_scan(self.scan.id)

        # Assertions
        self.assertEqual(result, f"Scan {self.scan.id} completed successfully.")

        # Refresh the scan object from the database
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'COMPLETED')
        self.assertIsNotNone(self.scan.completed_at)

        # Check that findings were created
        self.assertEqual(Finding.objects.count(), 2)
        finding1 = Finding.objects.get(rule_name='Test Rule 1')
        self.assertEqual(finding1.description, 'Test Description 1')
        self.assertEqual(finding1.level, 'danger')

    @patch('scout_web.api.services.run_from_api')
    def test_run_scan_failure(self, mock_run_from_api):
        # Mock the ScoutSuite API to raise an exception
        mock_run_from_api.side_effect = Exception("ScoutSuite API failed")

        # Call the service and expect an exception
        with self.assertRaises(Exception) as context:
            ScanService.run_scan(self.scan.id)

        self.assertTrue('ScoutSuite API failed' in str(context.exception))

        # Refresh the scan object from the database
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'FAILED')
        self.assertIsNotNone(self.scan.completed_at)
        self.assertEqual(Finding.objects.count(), 0)

    def test_run_scan_already_running(self):
        # Set the scan status to RUNNING
        self.scan.status = 'RUNNING'
        self.scan.save()

        # Call the service
        result = ScanService.run_scan(self.scan.id)

        # Assertions
        self.assertEqual(result, f"Scan {self.scan.id} is already in progress or completed.")
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'RUNNING')
        self.assertEqual(Finding.objects.count(), 0)

    @patch('scout_web.api.services.run_from_api')
    @patch('scout_web.api.models.Finding.objects.bulk_create')
    def test_run_scan_uses_bulk_create(self, mock_bulk_create, mock_run_from_api):
        # Mock the return value of the ScoutSuite API
        mock_findings = {
            'finding-1': {'rule_name': 'Test Rule 1', 'description': 'Test Description 1', 'level': 'danger'},
            'finding-2': {'rule_name': 'Test Rule 2', 'description': 'Test Description 2', 'level': 'warning'},
        }
        mock_cloud_provider = MagicMock()
        mock_cloud_provider.findings = mock_findings
        mock_run_from_api.return_value = mock_cloud_provider

        # Call the service
        ScanService.run_scan(self.scan.id)

        # Assert that bulk_create was called
        self.assertTrue(mock_bulk_create.called)
        self.assertEqual(mock_bulk_create.call_count, 1)
