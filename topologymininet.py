from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
import time
from config import HOST_CONFIGS

class IPv6TreeTopo(Topo):
    def build(self):
        # Add 3 Open vSwitches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')  # Core Switch
        s3 = self.addSwitch('s3')

        # Add 4 Hosts with specific IPv6 addresses
        h1 = self.addHost('h1', ip=HOST_CONFIGS['h1']['ip'])
        h2 = self.addHost('h2', ip=HOST_CONFIGS['h2']['ip'])
        h3 = self.addHost('h3', ip=HOST_CONFIGS['h3']['ip'])
        h4 = self.addHost('h4', ip=HOST_CONFIGS['h4']['ip'])

        # Establish Links
        self.addLink(h1, s1, bw=10, delay='1ms')
        self.addLink(h2, s1, bw=10, delay='1ms')
        self.addLink(s1, s2, bw=100, delay='2ms')
        self.addLink(s2, s3, bw=100, delay='2ms')
        self.addLink(h3, s3, bw=10, delay='1ms')
        self.addLink(h4, s3, bw=10, delay='1ms')

def start_network():
    setLogLevel('info')
    topo = IPv6TreeTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None) # Using OVS normal switching fallback
    net.start()

    info("*** Enabling IPv6 on all nodes...\n")
    for node in net.hosts + net.switches:
        node.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=0')
        node.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=0')
        node.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')

    info("*** Verifying Link Layer & internal routing...\n")
    time.sleep(2)  # Give Dad (Duplicate Address Detection) time to complete
    return net
