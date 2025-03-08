import os
import time

def block_ip(ip_address):
    """
    Blocks the malicious IP using iptables.
    """
    print(f"[ALERT] Blocking malicious IP: {ip_address}")
    try:
        # Block the IP using iptables (requires superuser privileges)
        os.system(f"sudo iptables -A INPUT -s {ip_address} -j DROP")
        print(f"IP {ip_address} has been blocked.")
    except Exception as e:
        print(f"Error blocking IP {ip_address}: {str(e)}")

def log_threat(ip_address):
    """
    Logs the blocked IP address into a log file.
    """
    with open("logs/threats.log", "a") as log_file:
        log_file.write(f"Blocked IP: {ip_address} at {time.ctime()}\n")
    print(f"[LOG] Threat from {ip_address} logged.")