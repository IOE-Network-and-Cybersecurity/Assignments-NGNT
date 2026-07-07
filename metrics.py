import subprocess
import re
import psutil
from config import HOST_CONFIGS

def collect_ping_metrics(net, src_name, dst_ip_raw):
    """Parses ping6 output to calculate Delay, PDR, and Packet Loss."""
    src_node = net.get(src_name)
    dst_ip = dst_ip_raw.split('/')[0]
    
    # Send 3 ICMPv6 packets
    cmd = f"ping6 -c 3 -W 2 {dst_ip}"
    result = src_node.cmd(cmd)
    
    # Regex parser patterns
    loss_pattern = re.search(r'(\d+)% packet loss', result)
    rtt_pattern = re.search(r'rtt min/avg/max/mdev = [\d\.]+/(缓慢|\d+\.\d+)/[\d\.]+/', result)
    
    packet_loss = float(loss_pattern.group(1)) if loss_pattern else 100.0
    pdr = 100.0 - packet_loss
    
    # Extract average delay
    if rtt_pattern:
        delay_ms = float(rtt_pattern.group(1))
    else:
        # Fallback manual catch if localized output differs
        avg_match = re.search(r'rtt min/avg/max/mdev = [0-9\.]+Dependencies/([0-9\.]+)', result)
        delay_ms = float(avg_match.group(1)) if avg_match else (0.0 if pdr > 0 else -1.0)

    return delay_ms, pdr, packet_loss

def get_system_resources():
    return psutil.cpu_percent(interval=None), psutil.virtual_memory().percent

def gather_all_metrics(net):
    metrics_summary = []
    
    # Test specific pairs representing Intraswitch (H1-H2) and Interswitch (H1-H3, H1-H4)
    pairs = [('h1', 'h2'), ('h1', 'h3'), ('h1', 'h4')]
    
    cpu, mem = get_system_resources()
    
    for src, dst in pairs:
        dst_ip = HOST_CONFIGS[dst]['ip']
        delay, pdr, loss = collect_ping_metrics(net, src, dst)
        
        # Approximate dynamic routing overhead and capacity footprint mocks for dashboard display
        bw_util = 5.0 + (pdr * 0.15) if pdr > 0 else 0.0 
        routing_overhead = 0.02 if pdr > 0 else 0.00
        
        metrics_summary.append({
            'host_pair': f"{src.upper()}-{dst.upper()}",
            'delay_ms': round(delay, 2),
            'pdr_percent': round(pdr, 2),
            'packet_loss': round(loss, 2),
            'bandwidth_percent': round(bw_util, 2),
            'routing_overhead': routing_overhead,
            'cpu_util': cpu,
            'memory_util': mem
        })
        
    return metrics_summary
