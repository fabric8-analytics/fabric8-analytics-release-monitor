"""Default configuration values."""
import os

NPM_URL = os.environ.get('NPM_URL', 'https://registry.npmjs.org/')  # type: str
PYPI_URL = os.environ.get('PYPI_URL', 'https://pypi.org/')  # type: str
ENABLE_SCHEDULING = os.environ.get('ENABLE_SCHEDULING', 'false').lower() in \
                    ('true', 'yes', '1')  # type: bool
# Sleep interval in minutes.
SLEEP_INTERVAL = int(os.environ.get('SLEEP_INTERVAL', 20))  # type: int
