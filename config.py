import os

# Network Configurations
IPv6_PREFIX = "2001:db8"
HOST_CONFIGS = {
    'h1': {'ip': f'{IPv6_PREFIX}:1::1/64', 'gw': f'{IPv6_PREFIX}:1::ff'},
    'h2': {'ip': f'{IPv6_PREFIX}:1::2/64', 'gw': f'{IPv6_PREFIX}:1::ff'},
    'h3': {'ip': f'{IPv6_PREFIX}:2::1/64', 'gw': f'{IPv6_PREFIX}:2::ff'},
    'h4': {'ip': f'{IPv6_PREFIX}:2::2/64', 'gw': f'{IPv6_PREFIX}:2::ff'},
}

# Monitoring Configurations
SAMPLING_INTERVAL = 2.0  # seconds
DASHBOARD_PORT = 5000

# Directory Setup
LOG_DIR = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

METRICS_CSV = os.path.join(LOG_DIR, 'metrics.csv')
EVENTS_LOG = os.path.join(LOG_DIR, 'events.log')
