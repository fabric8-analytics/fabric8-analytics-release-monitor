"""Default configuration values."""
import os

NPM_URL = os.environ.get('NPM_URL', 'https://registry.npmjs.org/')
PYPI_URL = os.environ.get('PYPI_URL', 'https://pypi.org/')
ENABLE_SCHEDULING = os.environ.get('ENABLE_SCHEDULING', 'true').lower() in ('true', 'yes', '1')
PROBE_FILE_LOCATION = "/tmp/release_monitoring/liveness.txt"
# Sleep interval in minutes.
SLEEP_INTERVAL = os.environ.get('SLEEP_INTERVAL', 20)
DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', 'yes', '1')
