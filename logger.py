import csv
import logging
from datetime import datetime
from config import METRICS_CSV, EVENTS_LOG

# Configure standard Logger
logging.basicConfig(filename=EVENTS_LOG, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def init_csv():
    with open(METRICS_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'host_pair', 'delay_ms', 'pdr_percent', 'bandwidth_percent', 'packet_loss', 'routing_overhead'])

def log_metrics_to_csv(metrics_list):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(METRICS_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        for m in metrics_list:
            writer.writerow([
                timestamp, m['host_pair'], m['delay_ms'], 
                m['pdr_percent'], m['bandwidth_percent'], m['packet_loss'], m['routing_overhead']
            ])
    logging.info(f"Metrics successfully written to CSV for {len(metrics_list)} pairs.")
