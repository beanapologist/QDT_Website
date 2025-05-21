from prometheus_client import Counter, Gauge, Histogram, Summary
from typing import Dict, List, Optional
import time
import psutil
import json
from datetime import datetime

class AccessibleMetrics:
    """Helper class for generating accessible metric descriptions"""
    @staticmethod
    def get_metric_description(metric_type: str, value: float) -> str:
        """Generate human-readable descriptions for metrics"""
        descriptions = {
            'cpu_percent': f"CPU usage is at {value}%",
            'memory_percent': f"Memory usage is at {value}%",
            'disk_usage': f"Disk usage is at {value}%",
            'network_io': f"Network I/O is at {value:.2f} MB"
        }
        return descriptions.get(metric_type, f"{metric_type}: {value}")

    @staticmethod
    def get_event_description(event_type: str, count: int) -> str:
        """Generate human-readable descriptions for events"""
        descriptions = {
            'User Login': f"{count} user login attempts",
            'User Logout': f"{count} user logout events",
            'File Access': f"{count} file access events",
            'Configuration Change': f"{count} configuration changes",
            'API Access': f"{count} API access events",
            'System Change': f"{count} system changes"
        }
        return descriptions.get(event_type, f"{count} {event_type} events")

# Security Metrics with user-friendly descriptions
SECURITY_EVENTS = Counter(
    'security_events_total',
    'Total number of security events by type and severity level',
    ['event_type', 'level'],
    documentation='Tracks security events such as login attempts, file access, and system changes'
)

AUTH_ATTEMPTS = Counter(
    'auth_attempts_total',
    'Total number of authentication attempts with success/failure status',
    ['status'],
    documentation='Monitors user login attempts to detect potential security threats'
)

HASH_VALIDATIONS = Counter(
    'hash_validations_total',
    'Total number of security hash validations with valid/invalid status',
    ['status'],
    documentation='Tracks the validation of security hashes for data integrity'
)

REQUEST_DURATION = Histogram(
    'request_duration_seconds',
    'Request duration in seconds by endpoint and method',
    ['endpoint', 'method'],
    documentation='Measures API response times to identify performance issues'
)

SYSTEM_METRICS = Gauge(
    'system_metrics',
    'System resource metrics including CPU and memory usage',
    ['metric_type'],
    documentation='Monitors system health and resource utilization'
)

ALERT_COUNTER = Counter(
    'security_alerts_total',
    'Total number of security alerts by severity level',
    ['level'],
    documentation='Tracks security alerts for monitoring and incident response'
)

class SecurityMetrics:
    def __init__(self):
        self._setup_metrics()
        self._last_update = time.time()
        self._update_interval = 5  # seconds
        self._metric_history: List[Dict] = []
        self._max_history = 100  # Keep last 100 metric updates

    def _setup_metrics(self):
        """Initialize metrics with default values and descriptions"""
        SYSTEM_METRICS.labels(metric_type='cpu_percent').set(0)
        SYSTEM_METRICS.labels(metric_type='memory_percent').set(0)
        SYSTEM_METRICS.labels(metric_type='memory_used').set(0)
        SYSTEM_METRICS.labels(metric_type='memory_total').set(0)
        SYSTEM_METRICS.labels(metric_type='disk_usage').set(0)
        SYSTEM_METRICS.labels(metric_type='network_io').set(0)

    def record_security_event(self, event_type: str, level: str = 'INFO'):
        """Record a security event with user-friendly event types"""
        event_types = {
            'login': 'User Login',
            'logout': 'User Logout',
            'file_access': 'File Access',
            'config_change': 'Configuration Change',
            'api_access': 'API Access',
            'system_change': 'System Change'
        }
        event_type = event_types.get(event_type, event_type)
        SECURITY_EVENTS.labels(event_type=event_type, level=level).inc()

    def record_auth_attempt(self, success: bool):
        """Record an authentication attempt with status"""
        status = 'success' if success else 'failure'
        AUTH_ATTEMPTS.labels(status=status).inc()

    def record_hash_validation(self, valid: bool):
        """Record a security hash validation with status"""
        status = 'valid' if valid else 'invalid'
        HASH_VALIDATIONS.labels(status=status).inc()

    def record_request_duration(self, endpoint: str, method: str, duration: float):
        """Record request duration with endpoint and method"""
        REQUEST_DURATION.labels(endpoint=endpoint, method=method).observe(duration)

    def update_system_metrics(self, metrics: Dict):
        """Update system metrics with comprehensive monitoring"""
        current_time = time.time()
        if current_time - self._last_update >= self._update_interval:
            # Update basic metrics
            SYSTEM_METRICS.labels(metric_type='cpu_percent').set(metrics['cpu_percent'])
            SYSTEM_METRICS.labels(metric_type='memory_percent').set(metrics['memory_percent'])
            SYSTEM_METRICS.labels(metric_type='memory_used').set(metrics['memory_used'])
            SYSTEM_METRICS.labels(metric_type='memory_total').set(metrics['memory_total'])

            # Update additional metrics
            disk_usage = psutil.disk_usage('/').percent
            SYSTEM_METRICS.labels(metric_type='disk_usage').set(disk_usage)

            net_io = psutil.net_io_counters()
            network_io = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024  # MB
            SYSTEM_METRICS.labels(metric_type='network_io').set(network_io)

            # Store metric history
            self._metric_history.append({
                'timestamp': datetime.utcnow().isoformat(),
                'metrics': metrics,
                'disk_usage': disk_usage,
                'network_io': network_io
            })
            if len(self._metric_history) > self._max_history:
                self._metric_history.pop(0)

            self._last_update = current_time

    def record_alert(self, level: str):
        """Record a security alert with severity level"""
        ALERT_COUNTER.labels(level=level).inc()

    def get_metrics_summary(self) -> Dict:
        """Get a user-friendly summary of all metrics"""
        return {
            'security_events': {
                'total': sum(SECURITY_EVENTS._value.get() for _ in SECURITY_EVENTS._metrics.values()),
                'by_type': {k: v for k, v in SECURITY_EVENTS._value.items()},
                'by_level': {k: v for k, v in SECURITY_EVENTS._value.items()},
                'descriptions': {
                    k: AccessibleMetrics.get_event_description(k, v)
                    for k, v in SECURITY_EVENTS._value.items()
                }
            },
            'auth_attempts': {
                'total': sum(AUTH_ATTEMPTS._value.get() for _ in AUTH_ATTEMPTS._metrics.values()),
                'success_rate': self._calculate_success_rate(),
                'description': f"Authentication success rate: {self._calculate_success_rate():.1f}%"
            },
            'system_health': {
                'cpu_usage': SYSTEM_METRICS._value.get('cpu_percent', 0),
                'memory_usage': SYSTEM_METRICS._value.get('memory_percent', 0),
                'disk_usage': SYSTEM_METRICS._value.get('disk_usage', 0),
                'descriptions': {
                    k: AccessibleMetrics.get_metric_description(k, v)
                    for k, v in {
                        'cpu_percent': SYSTEM_METRICS._value.get('cpu_percent', 0),
                        'memory_percent': SYSTEM_METRICS._value.get('memory_percent', 0),
                        'disk_usage': SYSTEM_METRICS._value.get('disk_usage', 0)
                    }.items()
                }
            },
            'alerts': {
                'total': sum(ALERT_COUNTER._value.get() for _ in ALERT_COUNTER._metrics.values()),
                'by_level': {k: v for k, v in ALERT_COUNTER._value.items()}
            },
            'history': self._metric_history
        }

    def _calculate_success_rate(self) -> float:
        """Calculate authentication success rate"""
        total = sum(AUTH_ATTEMPTS._value.get() for _ in AUTH_ATTEMPTS._metrics.values())
        if total == 0:
            return 0.0
        successes = AUTH_ATTEMPTS._value.get(('success',), 0)
        return (successes / total) * 100

    def get_accessible_metrics(self) -> str:
        """Generate an accessible text summary of all metrics"""
        summary = self.get_metrics_summary()
        return f"""
        System Status:
        {summary['system_health']['descriptions']['cpu_percent']}
        {summary['system_health']['descriptions']['memory_percent']}
        {summary['system_health']['descriptions']['disk_usage']}

        Security Events:
        {chr(10).join(summary['security_events']['descriptions'].values())}

        Authentication:
        {summary['auth_attempts']['description']}

        Alerts:
        Total alerts: {summary['alerts']['total']}
        """

class RequestTimer:
    def __init__(self, metrics: SecurityMetrics, endpoint: str, method: str):
        self.metrics = metrics
        self.endpoint = endpoint
        self.method = method
        self.start_time = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.metrics.record_request_duration(self.endpoint, self.method, duration) 