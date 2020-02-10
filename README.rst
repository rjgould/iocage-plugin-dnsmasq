######################
FreeNAS DNSMasq plugin
######################

This is an IOCage plugin for installing `DNSMasq <http://www.thekelleys.org.uk/dnsmasq/doc.html>`_ into FreeNAS (or TruOS).
It provides some configuration options via the (kind of) documented iocage interface.

This plugin is available for test, it has not yet been accepted into a RELEASE branch of the official `IOCage Plugins <https://github.com/freenas/iocage-ix-plugins>`_. To install use the following command::

    > iocage fetch -P --name dnsmasq ip4_addr="bge0|XXX.XXX.XXX.XXX/YY" --branch 'master'

Replacing *XXX.XXX.XXX.XXX/YY* with your preferred IP address and netmask.


Configuring dnsmasq
===================

This plugin applies some configuration defaults (see `post_install.sh` in this repository) to get you up and going. If you want to customise the configuration, changes can be made to `dnsmasq.conf` directly::

    # From host server
    > iocage console dnsmasq
    # Use vi to edit dnsmasq.conf
    > vi /usr/local/etc/dnsmasq.conf
    # Restart to apply
    > service dnsmasq restart
    # Use CTRL+D to exit back to host

All configuration files are in the default location `/usr/local/etc`.

.. note:: The `bind-interfaces` option is required for UDP DNS responses to work correctly.


IOCage Properties
=================

nameservers
-----------

Manage upstream nameservers. In these examples enable Google DNS servers

**set**::

    > iocage set -P nameservers=8.8.8.8,8.8.4.4 dnsmasq
    
**get**::

    > iocage get -P nameservers dnsmasq
    8.8.8.8,8.8.4.4

hostname entries
----------------

Add and remove host entries. 
   
**addhost**::
    
    > iocage set -P addhost=192.168.1.14,my_host_c dnsmasq
    
**delhost**::

    > iocage set -P delhost=my_host_c dnsmasq

**list**::

    > iocage get -P hosts dnsmasq
    192.168.1.10  my_host_a my_host_a_alt
    192.168.1.12  my_host_b
