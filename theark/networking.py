# Author: Micah Martin (knif3)
# toolbox.py
#
# Get a random IP address to use for the outbound connection
#

import random
import socket
import struct
from subprocess import Popen, PIPE
from ipaddress import IPv4Network

from . import app
from .toolbox import execute
from .arp import isIpTaken, _getIpFromDevice

config = app.config.get("networking", None)
if config is None:
    app.config['networking'] = {}
    config = app.config.get("networking")

LABEL = "ark"  # The label that new IPs are created with

## Functions that are to be called by other (sub)modules
def net_init():
    """Set up the networking stuff
    """
    if 'net_device' in config:
        config['base_ip'] = _getIpFromDevice(config['net_device'])
    else:
        config['base_ip'] = _getIp()
        config['inferface'] = _getInterfaceNameFromIp(config['base_ip'])
    config['netmask'] = _getSubnetMaskFromIp(config['base_ip'])  # Subnet mask

def discover_hosts(count=20):
    """Search through the network to discover COUNT number of IP addresses that are not in use
    This function calls arp.isIpTaken which will arp the network as its check.
    This function will also make sure the IP is not assigned to another tool by checking the database
    Args:
        count: The number of IP addresses to search for
    Returns:
        list[str]: the IPs that are up for use
    """
    # Get all the possible hosts in the network
    hosts = [ip.exploded for ip in IPv4Network(config['base_ip']+config['netmask'], strict=False).hosts()]
    random.shuffle(hosts)
    print("Discovering {} addresses to use...".format(count))
    addresses = set()
    # Keep looping until we run out of ip addresses or have found enough
    for ip in hosts:
        # Make sure the ip is not in use
        if isIpTaken(config['interface'], ip) \
            or app.config['DATABASE'].isIpTaken(ip) \
            or ip in addresses:
            continue
        # Add the ip to the list
        addresses.add(ip)
        if len(addresses) == count:
            break
    return list(addresses)

## Functions that are used internally not to be called by other modules
def _addVirtualInterface(ip, netmask, dev):
    '''
    add a virtual interface with the specified IP address

    Args:
        ip (str): The ip address to add
        dev (str): The dev to add the virtual interface to
    
    Returns:
        dict: the label of the new interface
    '''
    # Generate a label for the virtual interface
    label = "{}:{}{}".format(dev, LABEL, random.randint(1, 1000))
    while label in _getInterfaceLabels(dev):
        label = "{}:{}{}".format(dev, LABEL, random.randint(1, 1000))
    # Add the interface
    command = "ip addr add {}{} brd + dev {} label {}"
    command = command.format(ip, netmask, dev, label)
    res = execute(command)
    if res.get('status', 255) != 0:
        raise Exception("Cannot add interface: {}\n{}".format(
                        res.get('stderr', ''), command))
    return label


def _delVirtualInterface(ip, dev=None):
    '''
    delete a virtual interface with the specified IP address

    Args:
        ip (str): The ip address of the virtual interface
        dev (str, optional): the dev name
    '''
    if not dev:
        dev = _getInterfaceNameFromIp(ip)
    else:
        dev += ":*"
    netmask = _getSubnetMaskFromIp(ip)
    res = execute("ip addr del {}{} dev {}".format(ip, netmask, dev))
    if res.get('status', 255) != 0:
        raise Exception("Cannot delete interface: {}".format(
                        res.get('stderr', '')))
    return True


def _getInterfaceLabels(dev):
    '''
    return the labels of all virtual interfaces for a dev
    '''
    # The command to list all the labels assigned to an interface
    command = "".join(("ip a show dev {0} | grep -Eo '{0}:[a-zA-Z0-9:]+'",
                       " | cut -d':' -f2-"))
    # command = "ip a show dev {0}"
    command = command.format(dev)
    res = execute(command)
    try:
        labels = res['stdout'].strip().split()
        return labels
    except Exception:
        raise Exception("Cannot get labels: {}".format(res.get('stderr', '')))


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


