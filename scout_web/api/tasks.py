from celery import shared_task
from .models import Account, Scan, Finding
import datetime
from ScoutSuite.api import run_from_api

@shared_task
def run_scan(scan_id):
    """
    A Celery task to run a ScoutSuite scan.
    """
    scan = None
    try:
        scan = Scan.objects.get(id=scan_id)
        account = scan.account

        # Update the scan status to RUNNING
        scan.status = 'RUNNING'
        scan.save()

        # Run the scan using the new API function
        cloud_provider = run_from_api(provider=account.provider.code, **account.credentials)

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
