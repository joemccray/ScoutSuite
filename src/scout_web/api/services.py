import datetime
from .models import Scan, Finding
from ScoutSuite.api import run_from_api

class ScanService:
    @staticmethod
    def run_scan(scan_id):
        """
        This service runs a ScoutSuite scan for a given scan_id.
        """
        scan = None
        try:
            scan = Scan.objects.get(id=scan_id)

            # Check if the scan is already running or completed
            if scan.status != 'PENDING':
                return f"Scan {scan_id} is already in progress or completed."

            account = scan.account

            # Update the scan status to RUNNING
            scan.status = 'RUNNING'
            scan.save()

            # Prepare the arguments for the scan
            scan_args = {
                'provider': account.provider.code,
                **account.credentials,
                **scan.configuration,
            }

            # Run the scan using the new API function
            cloud_provider = run_from_api(**scan_args)

            # Process the findings
            if hasattr(cloud_provider, 'findings'):
                for finding_key, finding in cloud_provider.findings.items():
                    Finding.objects.create(
                        scan=scan,
                        rule_name=finding.get('rule_name', 'N/A'),
                        description=finding.get('description', ''),
                        level=finding.get('level', 'info'),
                        raw_finding=finding
                    )

            # Update the scan status to COMPLETED
            scan.status = 'COMPLETED'
            scan.completed_at = datetime.datetime.now(datetime.timezone.utc)
            scan.save()

            return f"Scan {scan_id} completed successfully."

        except Exception as e:
            if scan:
                scan.status = 'FAILED'
                scan.completed_at = datetime.datetime.now(datetime.timezone.utc)
                scan.save()

            print(f"Scan failed for scan_id {scan_id}: {e}")
            raise e
