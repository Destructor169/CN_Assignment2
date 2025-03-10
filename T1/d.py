from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

class CustomTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h7 = self.addHost('h7')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Add links with specific bandwidths and loss parameters
        self.addLink(h1, s1, bw=100)
        self.addLink(h2, s1, bw=100)
        self.addLink(h3, s2, bw=100)
        self.addLink(h4, s3, bw=100)
        self.addLink(h7, s4, bw=100)

        self.addLink(s1, s2, bw=100, loss=1)  # 1% loss
        self.addLink(s2, s3, bw=50, loss=5)   # 5% loss
        self.addLink(s3, s4, bw=100)

def runExperiment():
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
    net.start()

    # Start iperf server on h7
    h7 = net.get('h7')
    h7.cmd('iperf3 -s &')

    # Start iperf clients on h1, h2, h3, h4 with CUBIC, VEGAS, and HTCP
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')

    # Run iperf clients with CUBIC, VEGAS, and HTCP congestion control schemes
    h1.cmd('iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 150 -C cubic &')  # CUBIC
    h2.cmd('iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 150 -C vegas &')  # VEGAS
    h3.cmd('iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 150 -C htcp &')   # HTCP

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    runExperiment()
