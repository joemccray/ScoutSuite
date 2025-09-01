import asyncio
import tempfile

from ScoutSuite.core.console import print_info
from ScoutSuite.__main__ import _run


def run(provider: str, **kwargs):
    """
    Programmatic entry point for Scout Suite.

    :param provider:                Name of the cloud provider to be scouted
    :param kwargs:                  Dictionary of other options
    :return:
    """
    loop = asyncio.get_event_loop()
    _run_defaults = {
        'https': True, 'http': False, 'local': False, 'profile': None, 'regions': [], 'excluded_regions': [],
        'services': [], 'skipped_services': [], 'list_services': False, 'max_workers': 2, 'max_rate': 16, 'report_format': 'html',
        'report_name': None, 'report_dir': tempfile.gettempdir(), 'timestamp': False, 'ip_ranges_name_key': 'name',
        'ip_ranges_name_prefix': None, 'ip_ranges': [], 'fetch_local': False, 'force_write': False,
        'result_format': 'json', 'exceptions': None, 'ruleset': None, 'debug': False, 'quiet': False, 'log_file': None,
        'no_browser': False, 'credentials_file': None, 'project_id': None, 'project_name': None, 'subscription_id': None,
        'tenant_id': None, 'client_id': None, 'client_secret': None, 'refresh_token': None, 'domain': None,
        'username': None, 'password': None, 'key_path': None, 'ca_certs': None, 'user_auth': False, 'domain_name': None,
        'user_name': None, 'tenancy_id': None, 'user_id': None, 'fingerprint': None, 'config_file': None,
        'profile_name': None, 'cluster_details': None, 'cluster_name': None, 'all_clusters': False,
        'kube_config': None, 'config_path': None, 'context': None, 'inside_cluster': False, 'all_contexts': False,
        'kubernetes_version': None, 'kubernetes_config': None, 'kubernetes_in_cluster': False,
        'kubernetes_persist_config': True, 'kubernetes_azure_subscription_id': None, 'token': None,
        'access_key': None, 'access_secret': None, 'report_name': None, 'timestamp': False,
        'database_name': None,
        'host_ip': '127.0.0.1', 'host_port': 8000, 'update': False,
        'programmatic_execution': True,
    }

    # Combine defaults with provided kwargs
    run_args = {**_run_defaults, **kwargs, 'provider': provider}

    cloud_provider = loop.run_until_complete(_run(**run_args))
    loop.close()

    return cloud_provider
