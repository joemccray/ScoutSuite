import asyncio
from ScoutSuite.__main__ import _run

def run_from_api(provider, **kwargs):
    """
    This function will be the entry point for running a scan from the web API.
    It will set up the event loop and call the core _run function.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    _run_defaults = {
        'profile': None, 'aws_access_key_id': None, 'aws_secret_access_key': None, 'aws_session_token': None,
        'cli': False, 'user_account': False, 'user_account_browser': False, 'msi': False, 'service_principal': False, 'file_auth': None,
        'tenant_id': None, 'subscription_ids': None, 'all_subscriptions': None, 'client_id': None, 'client_secret': None,
        'username': None, 'password': None, 'service_account': None, 'project_id': None, 'folder_id': None,
        'organization_id': None, 'all_projects': False, 'access_key_id': None, 'access_key_secret': None,
        'kubernetes_cluster_provider': None, 'kubernetes_config_file': None, 'kubernetes_context': None,
        'kubernetes_persist_config': True, 'kubernetes_azure_subscription_id': None, 'token': None,
        'access_key': None, 'access_secret': None, 'report_name': None, 'report_dir': '/tmp', 'timestamp': False,
        'services': [], 'skipped_services': [], 'list_services': None, 'result_format': 'json', 'database_name': None,
        'host_ip': '127.0.0.1', 'host_port': 8000, 'regions': [], 'excluded_regions': [], 'fetch_local': False,
        'update': False, 'max_rate': None, 'ip_ranges': [], 'ip_ranges_name_key': 'name', 'ruleset': 'default.json',
        'exceptions': None, 'force_write': False, 'debug': False, 'quiet': True, 'log_file': None,
        'no_browser': True, 'programmatic_execution': True,
    }

    # Combine defaults with provided kwargs
    run_args = {**_run_defaults, **kwargs, 'provider': provider}

    cloud_provider = loop.run_until_complete(_run(**run_args))
    loop.close()

    return cloud_provider
