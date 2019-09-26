
"""
This class is basically a list of all the hosts that we know of.
You can blacklist hosts, add specific IP addresses/networks to the pool, 
and discover unused addresses in the pool
"""
import ipaddress
import random
import yaml
import socket

from .toolbox import execute
from .arp import isIpTaken


class Hosts(object):
    def __init__(self, config, database=None):
        self.hosts = []
        self.blacklist = set()
        self.config = config
        self.database = database


        # These need to be filled out for ARP to work
        self.base_ip = None
        self.interface = None
        self.netmask = None


    def is_ip_taken(self, ip):
        return isIpTaken(self.interface, self.base_ip, ip) or self.database.is_ip_taken(ip)


    def _update_net_settings(self, config):
        """
        Get/determine the base network settings from the config and the host machine,
        this is useful for ARP and for using the default settings
        """
        # If an interface is specified
        if config.get('interface', False):
            self.base_ip = _getIpFromDevice(config['interface'])
            self.interface = config['interface']
        else:
            self.base_ip = _getIp()
            self.interface = _getInterfaceNameFromIp(self.base_ip)
        self.netmask = _getSubnetMaskFromIp(self.base_ip)

    def clear_hosts(self):
        self.hosts = []
        self.blacklist = []
    
    def load_config(self):
        try:
            with open(self.config) as fil:
                config = yaml.safe_load(fil)
        except FileNotFoundError:
            print("'config.yml' not found. Using Default network only")
            config = {}
        return config

    def build_hosts(self):
        """Parse through all the networks and get all possible hosts
        """
        self.hosts = set()
        self.blacklist = set()
        config = self.load_config()
        self._update_net_settings(config)

        # Get all the invalid hosts
        for network in config.get("invalid", []):
            # Handle networks
            if "/" in network:
                for ip in ipaddress.ip_network(network, strict=False).hosts():
                    self.blacklist.add(ip.exploded)
                continue
            # Handle blank IP addresses
            self.blacklist.add(network)

        # Get all the valid hosts
        for network in config.get("valid", ["default"]):
            # Handle the defualt network (whatever the box has)
            if network == "default":
                network = "{}{}".format(self.base_ip, self.netmask)
            # Handle networks
            if "/" in network:
                for ip in ipaddress.ip_network(network, strict=False).hosts():
                    if ip not in self.blacklist:
                        self.hosts.add(ip.exploded)
                continue
            # Handle single IP addresses
            if network not in self.blacklist:
                self.hosts.add(network)
            self.hosts = list(self.hosts)

    def discover_hosts(self, count=20):
        print("Discovering {} addresses to use...".format(count))
        # Rebuild all the hosts here. This may seem like redundant calculations
        # However it achieves two goals:
        #   1. It uses less RAM _most_ of the time
        #   2. It allows the config to be dynamically changed
        #   3. We dont really have too many services that register
        self.build_hosts()
        random.shuffle(self.hosts)
        addresses = set()
        # Keep looping until we run out of ip addresses or have found enough
        for addr in self.hosts:
            # Make sure the ip is not in use
            if self.is_ip_taken(addr) or addr in addresses:
                continue
            # Add the ip to the list
            addresses.add(addr)
            if len(addresses) == count:
                break
        # Clear these so we get our memory back
        self.clear_hosts()
        return list(addresses)


def _getIp(host="1.1.1.1"):
    """Get the ip address that would be used to connect to this host

    Args:
        host (str): the host to connect to, default to an external host
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect((host,1))
    ip = soc.getsockname()[0]
    soc.close()
    return ip


def _getSubnetMaskFromIp(ip):
    """Get the subnet mask for the given IP

    Args:
        ip (str): the ip address
    Returns:
        str: the subnet mask
    """
    res = execute("ip addr | grep -oE '{}/[^ ]+'".format(ip))  # Get three lines of output
    if res.get('status', 255) != 0:
        raise Exception("Cannot find default interface: {}".format(res.get('stderr', '')))
    mask = res['stdout'].split("/")[-1].strip()
    return "/" + mask


def _getInterfaceNameFromIp(ip):
    """Given an IP address, return the interface name the is associated with it

    Args:
        ip (str): the ip address
    Returns:
        str: the interface name
    """
    res = execute("ip addr | grep '{}' -B2".format(ip))  # Get three lines of output
    if res.get('status', 255) != 0:
        raise Exception("Cannot find default interface: {}".format(res.get('stderr', '')))
    dev = res['stdout'].split()[-1].strip()
    if dev == "dynamic":
        dev = res['stdout'].split("\n")[0].split()[1].strip(":")
    return dev

def _getIpFromDevice(dev):
    """Get the ip address of a device
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, 25, (dev+'\0').encode())
    sock.connect(("1.1.1.1",1))
    ip = sock.getsockname()[0]
    sock.close()
    return ip