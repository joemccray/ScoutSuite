import os, sys, pathlib, pytest
# Ensure repo root on sys.path
ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Block network by default (pytest-socket if available)
try:
    import pytest_socket  # type: ignore
    pytest_plugins = ("pytest_socket",)
    def pytest_runtest_setup(item):
        from pytest_socket import disable_socket
        disable_socket()
except Exception:
    pass

# AWS safety
os.environ.setdefault("AWS_EC2_METADATA_DISABLED", "true")
os.environ.setdefault("BOTO_CONFIG", "/dev/null")
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")

@pytest.fixture
def enable_network():
    """Opt-in network access when a test truly needs it."""
    from pytest_socket import enable_socket
    enable_socket()
