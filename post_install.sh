#!/bin/sh -x

# Copy resolve.conf to provide initial config
cp /etc/resolve.conf /usr/local/etc/resolve.conf

# Apply settings to dnsmasq.conf
sed -i s/#bind-interfaces/bind-interfaces/g
sed -i s/#resolve-file=/resolve-file=\/usr\/local\/etc\/resolve.conf/g

# Enable the service
sysrc -f /etc/rc.conf dnsmasq_enable="YES"

# Start the service
service dnsmasq start 2>/dev/null

echo "dnsmasq now installed" > /root/PLUGIN_INFO
