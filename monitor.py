import threading
import time
from flask import Flask, jsonify
from mininet.cli import CLI
import topology
import metrics
import logger
import config

app = Flask(__name__)
latest_runtime_cache = []

@app.route('/api/metrics', methods=['GET'])
def get_metrics_api():
    return jsonify({
        "status": "success",
        "data": latest_runtime_cache
    })

def background_monitoring_loop(net):
    global latest_runtime_cache
    logger.init_csv()
    logger.logging.info("Network engine monitoring loop started.")
    
    while True:
        try:
            data = metrics.gather_all_metrics(net)
            latest_runtime_cache = data
            logger.log_metrics_to_csv(data)
        except Exception as e:
            logger.logging.error(f"Error encountered in telemetry thread: {str(e)}")
        time.sleep(config.SAMPLING_INTERVAL)

if __name__ == '__main__':
    # 1. Initialize Network Topology
    net = topology.start_network()
    
    # 2. Start Telemetry Thread
    monitor_thread = threading.Thread(target=background_monitoring_loop, args=(net,))
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # 3. Start Flask REST API Server asynchronously 
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=config.DASHBOARD_PORT, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    print(f"\n*** Web API Server streaming live at: http://localhost:{config.DASHBOARD_PORT}/api/metrics")
    print("*** Launching Mininet interactive CLI environment. Type 'exit' to wind down. ***\n")
    
    # 4. Open interactive CLI console
    CLI(net)
    
    # 5. Safe Cleanup on termination
    print("*** Shitting down network services and closing engine links...")
    net.stop()
