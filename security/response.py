import os
import platform
import time
from datetime import datetime, timedelta
import json
from config import SECURITY_CONFIG
from utils.logger import logger

class SecurityResponse:
    def __init__(self):
        self.blocked_ips = {}
        self.attempts = {}
        self.system = platform.system().lower()

    def _is_valid_ip(self, ip_address):
        """Validate IP address format."""
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

    def _get_block_command(self, ip_address):
        """Get platform-specific block command."""
        if self.system == 'linux':
            return f"sudo iptables -A INPUT -s {ip_address} -j DROP"
        elif self.system == 'windows':
            return f'netsh advfirewall firewall add rule name="Block IP {ip_address}" dir=in action=block remoteip={ip_address} enable=yes'
        else:
            raise NotImplementedError(f"Platform {self.system} not supported")

    def _get_unblock_command(self, ip_address):
        """Get platform-specific unblock command."""
        if self.system == 'linux':
            return f"sudo iptables -D INPUT -s {ip_address} -j DROP"
        elif self.system == 'windows':
            return f'netsh advfirewall firewall delete rule name="Block IP {ip_address}"'
        else:
            raise NotImplementedError(f"Platform {self.system} not supported")

    def block_ip(self, ip_address, duration=None, reason=None):
        """Block an IP address with optional duration."""
        if not self._is_valid_ip(ip_address):
            logger.error(f"Invalid IP address format: {ip_address}")
            return False

        try:
            if duration is None:
                duration = SECURITY_CONFIG['block_duration']

            block_time = datetime.now()
            unblock_time = block_time + timedelta(seconds=duration)

            # Execute block command
            block_command = self._get_block_command(ip_address)
            logger.info(f"Executing command: {block_command}")
            result = os.system(block_command)
            
            if result != 0:
                logger.error(f"Failed to execute firewall command. Exit code: {result}")
                return False

            # Update blocked IPs registry
            self.blocked_ips[ip_address] = {
                'block_time': block_time.isoformat(),
                'unblock_time': unblock_time.isoformat(),
                'reason': reason
            }

            # Log the action
            logger.log_threat(
                ip_address,
                'IP_BLOCKED',
                {
                    'duration': duration,
                    'reason': reason,
                    'permanent': duration == 0
                }
            )

            # Schedule unblock if temporary
            if duration > 0:
                time.sleep(duration)
                self.unblock_ip(ip_address)

            return True
        except Exception as e:
            logger.error(f"Failed to block IP {ip_address}: {str(e)}")
            return False

    def unblock_ip(self, ip_address):
        """Unblock a previously blocked IP address."""
        try:
            if ip_address in self.blocked_ips:
                unblock_command = self._get_unblock_command(ip_address)
                logger.info(f"Executing command: {unblock_command}")
                result = os.system(unblock_command)
                
                if result != 0:
                    logger.error(f"Failed to execute firewall command. Exit code: {result}")
                    return False
                
                del self.blocked_ips[ip_address]
                logger.info(f"IP {ip_address} has been unblocked")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to unblock IP {ip_address}: {str(e)}")
            return False

    def is_blocked(self, ip_address):
        """Check if an IP is currently blocked."""
        if ip_address not in self.blocked_ips:
            return False

        block_info = self.blocked_ips[ip_address]
        unblock_time = datetime.fromisoformat(block_info['unblock_time'])
        
        if datetime.now() > unblock_time:
            self.unblock_ip(ip_address)
            return False
        
        return True

    def get_blocked_ips(self):
        """Get list of currently blocked IPs."""
        return self.blocked_ips

# Create a singleton instance
security_response = SecurityResponse() 
