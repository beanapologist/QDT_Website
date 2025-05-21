import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
import psutil
import redis
from src.security.qdt_security import QDTSecurityCore

class SecurityMonitor:
    def __init__(self, redis_client: redis.Redis):
        self.core = QDTSecurityCore()
        self.redis = redis_client
        self.logger = self._setup_logger()
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'failed_auth_attempts': 5,
            'invalid_hash_attempts': 3
        }

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('security_monitor')
        logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler('security.log')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def log_security_event(self, event_type: str, details: Dict) -> None:
        """Log security events with timestamp and details"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': event_type,
            'details': details
        }
        self.logger.info(f"Security Event: {event}")
        self.redis.lpush('security_events', str(event))
        self.redis.ltrim('security_events', 0, 999)  # Keep last 1000 events

    def check_system_resources(self) -> Dict:
        """Monitor system resources"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        metrics = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used': memory.used,
            'memory_total': memory.total
        }
        
        if cpu_percent > self.alert_thresholds['cpu_percent']:
            self.log_security_event('high_cpu_usage', metrics)
        
        if memory.percent > self.alert_thresholds['memory_percent']:
            self.log_security_event('high_memory_usage', metrics)
        
        return metrics

    def track_auth_attempt(self, user_key: str, success: bool) -> None:
        """Track authentication attempts"""
        key = f"auth_attempts:{user_key}"
        if not success:
            attempts = self.redis.incr(key)
            self.redis.expire(key, 3600)  # Expire after 1 hour
            
            if attempts >= self.alert_thresholds['failed_auth_attempts']:
                self.log_security_event('suspicious_auth_attempts', {
                    'user_key': user_key,
                    'attempts': attempts
                })
        else:
            self.redis.delete(key)

    def track_hash_validation(self, hash_value: str, valid: bool) -> None:
        """Track security hash validation attempts"""
        if not valid:
            key = f"invalid_hash_attempts:{hash_value}"
            attempts = self.redis.incr(key)
            self.redis.expire(key, 3600)
            
            if attempts >= self.alert_thresholds['invalid_hash_attempts']:
                self.log_security_event('suspicious_hash_attempts', {
                    'hash': hash_value,
                    'attempts': attempts
                })

    def get_security_events(self, limit: int = 100) -> List[Dict]:
        """Retrieve recent security events"""
        events = self.redis.lrange('security_events', 0, limit - 1)
        return [eval(event.decode()) for event in events]

    def get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': self.check_system_resources(),
            'security_events_count': self.redis.llen('security_events')
        }

class SecurityAlert:
    def __init__(self, monitor: SecurityMonitor):
        self.monitor = monitor
        self.alert_levels = {
            'INFO': 0,
            'WARNING': 1,
            'CRITICAL': 2
        }

    def send_alert(self, level: str, message: str) -> None:
        """Send security alerts"""
        if level not in self.alert_levels:
            raise ValueError(f"Invalid alert level: {level}")
        
        alert = {
            'level': level,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.monitor.log_security_event('security_alert', alert)
        
        if self.alert_levels[level] >= self.alert_levels['WARNING']:
            # Here you would integrate with your alerting system
            # (e.g., email, Slack, PagerDuty)
            pass 