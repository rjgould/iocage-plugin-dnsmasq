#!/bin/sh -x

# Enable the service
sysrc -f /etc/rc.conf dnsmasq_enable="YES"

# Start the service
service dnsmasq start 2>/dev/null

echo "dnsmasq now installed" > /root/PLUGIN_INFO
