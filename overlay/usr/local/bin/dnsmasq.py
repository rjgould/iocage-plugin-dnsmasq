"""
Common methods for dnsmasq get/set
"""
from pathlib import Path
from collections import defaultdict


# Conf file locations
HOSTS = Path("/etc/hosts")
RESOLV_CONF = Path("/etc/resolv.conf")
DNSMASQ_CONF = Path("/usr/local/etc/dnsmasq.conf")


# IP addresses to filter out
SPECIAL_IPS = (
    '127.0.0.1',  # Local host
    '127.0.1.1',  # Current machine
    '::1',        # Local host (IPv6)
    'fe00::0',    # Local net (IPv6)
    'ff00::0',    # MCast prefix (IPv6)
    'ff02::1',    # All Nodes (IPv6)
    'ff02::2',    # All Routers (IPv6)
)


class NameServers(list):
    """
    Read/modify name servers
    """
    def __str__(self):
        return ", ".join(self)

    def read(self, file=None):
        file = file or RESOLV_CONF

        with file.open() as f:
            self.clear()
            for line in f:
                line = line.strip()
                if line.startswith("nameserver"):
                    self.append(line[11:].strip())

        return self

    def write(self, file=None):
        file = file or RESOLV_CONF

        # Read in current file
        with file.open() as f:
            existing = [
                line for line in f
                if not line.strip().startswith("nameserver")
            ]

        for server in self:
            existing.append(f"nameserver {server}\n")

        with file.open('w') as f:
            f.writelines(existing)


class Hosts:
    """
    Read/modify the hosts file
    """
    def __init__(self, entries=None):
        self._entries = defaultdict(set)
        if entries:
            self._entries.update(entries)

    def __str__(self):
        return "\n".join(
            f"{ip}\t{' '.join(host_names)}"
            for ip, host_names in self._entries.items()
        )

    def read(self, file=None):
        """
        Read in from hosts file
        """
        file = file or HOSTS
        entries = self._entries

        with file.open() as f:
            entries.clear()
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ip, *host_names = line.split()
                    entries[ip].update(host_names)

        return self

    def write(self, file=None):
        """
        Write out to hosts file
        """
        file = file or HOSTS

        with file.open('w') as f:
            f.writelines(
                f"{ip}\t{' '.join(host_names)}\n"
                for ip, host_names in self._entries.items()
            )

    def add(self, ip, host_name):
        """
        Add an entry
        """
        self._entries[ip].add(host_name)
        return self

    def remove(self, host_name):
        """
        Remove a host name
        """
        orphaned_ips = []
        for ip, host_names in self._entries.items():
            if host_name in host_names:
                host_names.remove(host_name)
                if len(host_names) == 0:
                    orphaned_ips.append(ip)

        # Remove orphans
        for ip in orphaned_ips:
            del self._entries[ip]

        return self

    def filter(self, black_list=SPECIAL_IPS):
        """
        Filter out ips on a black list
        """
        entries = self._entries
        return Hosts(
            {ip: entries[ip] for ip in entries if ip not in black_list}
        )
