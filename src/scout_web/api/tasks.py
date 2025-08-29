from celery import shared_task
from .services import ScanService

@shared_task(ignore_result=True)
def run_scan(scan_id):
    """
    A Celery task to run a ScoutSuite scan.
    This task is a thin wrapper around the ScanService.
    """
    ScanService.run_scan(scan_id)
