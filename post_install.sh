#!/bin/sh -x

DNSMASQ_CONF=/usr/local/etc/dnsmasq.conf

# Copy resolve.conf to provide initial config
cp /etc/resolv.conf /usr/local/etc/resolv.conf

# Apply settings to dnsmasq.conf
sed -i -e 's/#bind-interfaces/bind-interfaces/g' ${DNSMASQ_CONF}
sed -i -e 's/#resolv-file=/resolv-file=\/usr\/local\/etc\/resolv.conf/g' ${DNSMASQ_CONF}

# Enable the service
sysrc -f /etc/rc.conf dnsmasq_enable="YES"

# Start the service
service dnsmasq start 2>/dev/null

echo "dnsmasq now installed" > /root/PLUGIN_INFO
