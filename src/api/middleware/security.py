from functools import wraps
from flask import request, jsonify
from src.security.qdt_security import QDTSecurityCore, QDTAccessControl
from src.security.monitoring import SecurityMonitor, SecurityAlert
import redis
import time

# Initialize Redis client
redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)

# Initialize security components
security_core = QDTSecurityCore()
access_control = QDTAccessControl(security_core)
security_monitor = SecurityMonitor(redis_client)
security_alert = SecurityAlert(security_monitor)

def require_auth(level='PRIME_HUNTER'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                security_monitor.log_security_event('missing_auth_header', {
                    'ip': request.remote_addr,
                    'path': request.path
                })
                return jsonify({'error': 'No authorization header'}), 401

            try:
                user_key = auth_header.split(' ')[1]
                challenge = request.headers.get('X-Challenge', '0')
                access_level = access_control.authenticate_user(user_key, challenge)
                
                # Track authentication attempt
                security_monitor.track_auth_attempt(
                    user_key,
                    access_level >= access_control.access_levels[level]
                )
                
                if access_level < access_control.access_levels[level]:
                    security_alert.send_alert(
                        'WARNING',
                        f'Failed access attempt for level {level} from {request.remote_addr}'
                    )
                    return jsonify({'error': 'Insufficient access level'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                security_monitor.log_security_event('auth_error', {
                    'error': str(e),
                    'ip': request.remote_addr
                })
                return jsonify({'error': str(e)}), 401
                
        return decorated_function
    return decorator

def validate_request():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Validate request security hash
            security_hash = request.headers.get('X-Security-Hash')
            expected_hash = security_core._generate_security_hash()
            
            # Track hash validation
            security_monitor.track_hash_validation(
                security_hash or '',
                security_hash == expected_hash
            )
            
            if not security_hash or security_hash != expected_hash:
                security_alert.send_alert(
                    'WARNING',
                    f'Invalid security hash from {request.remote_addr}'
                )
                return jsonify({'error': 'Invalid security hash'}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def monitor_request():
    """Middleware to monitor all requests"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            # Check system resources before processing
            metrics = security_monitor.check_system_resources()
            if metrics['cpu_percent'] > 90 or metrics['memory_percent'] > 90:
                security_alert.send_alert(
                    'CRITICAL',
                    f'High resource usage: CPU {metrics["cpu_percent"]}%, Memory {metrics["memory_percent"]}%'
                )
            
            try:
                response = f(*args, **kwargs)
                processing_time = time.time() - start_time
                
                # Log request details
                security_monitor.log_security_event('request_processed', {
                    'path': request.path,
                    'method': request.method,
                    'ip': request.remote_addr,
                    'processing_time': processing_time,
                    'status_code': response.status_code
                })
                
                return response
            except Exception as e:
                security_monitor.log_security_event('request_error', {
                    'path': request.path,
                    'error': str(e),
                    'ip': request.remote_addr
                })
                raise
                
        return decorated_function
    return decorator 