import datetime
from .models import Scan, Finding
from ScoutSuite.api import run as run_from_api
import logging

class ScanService:
    @staticmethod
    def run_scan(scan_id: int) -> str:
        """
        This service runs a ScoutSuite scan for a given scan_id.

        :param scan_id: The ID of the scan to run.
        :return: A string indicating the result of the scan.
        """
        scan = None
        try:
            scan = Scan.objects.get(id=scan_id)

            # Check if the scan is already running or completed
            if scan.status != 'PENDING':
                logging.warning(f"Scan {scan_id} is not in PENDING state (current state: {scan.status}). Aborting.")
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
            if hasattr(cloud_provider, 'findings') and cloud_provider.findings:
                findings_to_create = []
                for finding_key, finding_data in cloud_provider.findings.items():
                    findings_to_create.append(
                        Finding(
                            scan=scan,
                            rule_name=finding_data.get('rule_name', 'N/A'),
                            description=finding_data.get('description', ''),
                            level=finding_data.get('level', 'info'),
                            raw_finding=finding_data
                        )
                    )
                if findings_to_create:
                    Finding.objects.bulk_create(findings_to_create)

            # Update the scan status to COMPLETED
            scan.status = 'COMPLETED'
            scan.completed_at = datetime.datetime.now(datetime.timezone.utc)
            scan.save()

            logging.info(f"Scan {scan_id} completed successfully.")
            return f"Scan {scan_id} completed successfully."

        except Scan.DoesNotExist:
            logging.error(f"Scan with id {scan_id} not found.")
            raise
        except Exception as e:
            logging.error(f"Scan failed for scan_id {scan_id}: {e}", exc_info=True)
            if scan:
                scan.status = 'FAILED'
                scan.completed_at = datetime.datetime.now(datetime.timezone.utc)
                scan.save()
            raise e
