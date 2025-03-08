import os

def block_ip(ip_address):
    """
    Blocks the IP using iptables.
    """
    try:
        print(f"[FIREWALL] Blocking IP: {ip_address}")
        # Run iptables command to block the IP address
        os.system(f"sudo iptables -A INPUT -s {ip_address} -j DROP")
        print(f"Blocked IP: {ip_address}")
    except Exception as e:
        print(f"[ERROR] Failed to block IP {ip_address}: {e}")