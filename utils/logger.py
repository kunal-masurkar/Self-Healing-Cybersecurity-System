import logging
import os
from datetime import datetime
from config import LOG_CONFIG

class SystemLogger:
    def __init__(self):
        self.logger = logging.getLogger('security_system')
        self.logger.setLevel(LOG_CONFIG['level'])
        
        # Create formatters
        formatter = logging.Formatter(LOG_CONFIG['format'])
        
        # File handler
        file_handler = logging.FileHandler(LOG_CONFIG['file'])
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def log_threat(self, ip_address, threat_type, details):
        threat_log = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'threat_type': threat_type,
            'details': details
        }
        self.info(f"Threat detected: {threat_log}")

# Create a singleton instance
logger = SystemLogger() 
