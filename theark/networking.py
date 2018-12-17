#
# Author: Micah Martin (knif3)
#
# ips.py
# 
# Manage all the creation, finding, searching, and calculations for ips and virtual ips
#

import os
import socket
import random

from .toolbox import execute
from . import app

CONFIG = app.config.get("networking", {})

def addInterface(ip, label=None, dev=None):
    '''
    add a virtual interface with the specified IP address
    Returns: label - the label of the new interface
    '''
    if not dev:
        dev = CONFIG.get("interface", "eth0")
    # Generate a label for the virtual interface
    label = "{}:ark{}".format(dev, random.randint(1, 1000))
    while label in getInterfaceLabels(dev):
        label = "{}:ark{}".format(dev, random.randint(1, 1000))

    # Add the interface
    command = "ip addr add {}/24 brd + dev {} label {}"
    command = command.format(ip, dev, label)
    res = execute(command)
    if res.get('status', 255) != 0:
        raise Exception("Cannot add interface: {}\n{}".format(
                        res.get('stderr', ''), command))
    return {'label': label, 'ip': ip}


def delInterface(ip, dev=None):
    '''
    delete a virtual interface with the specified IP address
    '''
    if not dev:
        dev = CONFIG.get("interface", "eth0")
    res = execute("ip addr del {}/24 dev {}:*".format(ip, dev))
    if res.get('status', 255) != 0:
        raise Exception("Cannot delete interface: {}".format(
                        res.get('stderr', '')))
    return True

def getInterfaceLabels(dev=None):
    '''
    return the labels of all virtual interfaces for a dev
    '''
    # If the device is not specified, use the device in the config
    if not dev:
        dev = CONFIG.get("interface", "eth0")
    # The command to list all the labels assigned to an interface
    command = "".join(("ip a show dev {0} | grep -Eo '{0}:[a-zA-Z0-9:]+'",
                       " | cut -d':' -f2-"))
    # command = "ip a show dev {0}"
    command = command.format(dev)
    res = execute(command)
    try:
        labels = res['stdout'].strip().split()
        return labels
    except Exception as E:
        raise Exception("Cannot get labels: {}".format(res.get('stderr', '')))

def getIp():
    """Find the IP address that is used as the default interface

    Returns:
        string: the default IP address
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect(("1.1.1.1",1))
    ip = soc.getsockname()[0]
    soc.close()
    return ip

def getInterfaceNameFromIp(ip):
    """Given an IP address, return the interface name the is associated with it
    """
    res = execute("ip addr | grep '{}' -B2 | head -n 1".format(ip))
    if res.get('status', 255) != 0:
        raise Exception("Cannot find default interface: {}".format(res.get('stderr', '')))
    return res['stdout'].split()[1].strip(":")
