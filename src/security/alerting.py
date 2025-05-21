import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from typing import Dict, Optional, List
from datetime import datetime
import time
import json
import html

class AlertSender:
    def __init__(self):
        self.email_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'username': os.getenv('SMTP_USERNAME'),
            'password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('ALERT_FROM_EMAIL'),
            'to_email': os.getenv('ALERT_TO_EMAIL')
        }
        
        self.slack_config = {
            'webhook_url': os.getenv('SLACK_WEBHOOK_URL')
        }
        
        self.pagerduty_config = {
            'api_key': os.getenv('PAGERDUTY_API_KEY'),
            'service_id': os.getenv('PAGERDUTY_SERVICE_ID')
        }

        # Alert templates with accessibility considerations
        self.alert_templates = {
            'system': {
                'title': 'System Alert',
                'template': """
                🚨 System Alert
                Level: {level}
                Time: {time}
                
                {message}
                
                System Status:
                - CPU Usage: {cpu_usage}%
                - Memory Usage: {memory_usage}%
                - Disk Usage: {disk_usage}%
                
                Please check the system dashboard for more details.
                """,
                'html_template': """
                <div role="alert" aria-live="polite">
                    <h2>🚨 System Alert</h2>
                    <p><strong>Level:</strong> {level}</p>
                    <p><strong>Time:</strong> {time}</p>
                    <p>{message}</p>
                    <h3>System Status:</h3>
                    <ul>
                        <li>CPU Usage: {cpu_usage}%</li>
                        <li>Memory Usage: {memory_usage}%</li>
                        <li>Disk Usage: {disk_usage}%</li>
                    </ul>
                    <p>Please check the system dashboard for more details.</p>
                </div>
                """
            },
            'security': {
                'title': 'Security Alert',
                'template': """
                🔒 Security Alert
                Level: {level}
                Time: {time}
                
                {message}
                
                Security Status:
                - Event Type: {event_type}
                - Location: {location}
                - User: {user}
                
                Please review the security dashboard for more information.
                """,
                'html_template': """
                <div role="alert" aria-live="polite">
                    <h2>🔒 Security Alert</h2>
                    <p><strong>Level:</strong> {level}</p>
                    <p><strong>Time:</strong> {time}</p>
                    <p>{message}</p>
                    <h3>Security Status:</h3>
                    <ul>
                        <li>Event Type: {event_type}</li>
                        <li>Location: {location}</li>
                        <li>User: {user}</li>
                    </ul>
                    <p>Please review the security dashboard for more information.</p>
                </div>
                """
            },
            'performance': {
                'title': 'Performance Alert',
                'template': """
                ⚡ Performance Alert
                Level: {level}
                Time: {time}
                
                {message}
                
                Performance Metrics:
                - Response Time: {response_time}ms
                - Error Rate: {error_rate}%
                - Request Count: {request_count}
                
                Check the performance dashboard for detailed metrics.
                """,
                'html_template': """
                <div role="alert" aria-live="polite">
                    <h2>⚡ Performance Alert</h2>
                    <p><strong>Level:</strong> {level}</p>
                    <p><strong>Time:</strong> {time}</p>
                    <p>{message}</p>
                    <h3>Performance Metrics:</h3>
                    <ul>
                        <li>Response Time: {response_time}ms</li>
                        <li>Error Rate: {error_rate}%</li>
                        <li>Request Count: {request_count}</li>
                    </ul>
                    <p>Check the performance dashboard for detailed metrics.</p>
                </div>
                """
            }
        }

        # Alert history for tracking
        self._alert_history: List[Dict] = []
        self._max_history = 1000  # Keep last 1000 alerts

    def _format_alert_message(self, alert_type: str, level: str, message: str, **kwargs) -> Dict[str, str]:
        """Format alert message using templates for different formats"""
        template = self.alert_templates.get(alert_type, self.alert_templates['system'])
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Format for plain text
        plain_text = template['template'].format(
            level=level,
            time=timestamp,
            message=message,
            **kwargs
        )
        
        # Format for HTML
        html_text = template['html_template'].format(
            level=html.escape(level),
            time=html.escape(timestamp),
            message=html.escape(message),
            **{k: html.escape(str(v)) for k, v in kwargs.items()}
        )
        
        return {
            'plain_text': plain_text,
            'html': html_text
        }

    def _record_alert(self, alert_type: str, level: str, message: str, **kwargs):
        """Record alert in history"""
        self._alert_history.append({
            'type': alert_type,
            'level': level,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
            'details': kwargs
        })
        if len(self._alert_history) > self._max_history:
            self._alert_history.pop(0)

    def send_email_alert(self, level: str, message: str, alert_type: str = 'system', **kwargs) -> bool:
        """Send alert via email with formatted message"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = f"QDT {self.alert_templates[alert_type]['title']} - {level}"
            
            formatted = self._format_alert_message(alert_type, level, message, **kwargs)
            msg.attach(MIMEText(formatted['plain_text'], 'plain'))
            msg.attach(MIMEText(formatted['html'], 'html'))
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
            
            self._record_alert(alert_type, level, message, **kwargs)
            return True
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")
            return False

    def send_slack_alert(self, level: str, message: str, alert_type: str = 'system', **kwargs) -> bool:
        """Send alert to Slack with formatted message"""
        try:
            if not self.slack_config['webhook_url']:
                return False
                
            color = {
                'INFO': '#36a64f',
                'WARNING': '#ffcc00',
                'CRITICAL': '#ff0000'
            }.get(level, '#36a64f')
            
            formatted = self._format_alert_message(alert_type, level, message, **kwargs)
            
            payload = {
                'attachments': [{
                    'color': color,
                    'title': f"QDT {self.alert_templates[alert_type]['title']} - {level}",
                    'text': formatted['plain_text'],
                    'ts': int(time.time()),
                    'footer': 'QDT Security System',
                    'footer_icon': 'https://your-domain.com/security-icon.png',
                    'mrkdwn_in': ['text']
                }]
            }
            
            response = requests.post(
                self.slack_config['webhook_url'],
                json=payload
            )
            
            if response.status_code == 200:
                self._record_alert(alert_type, level, message, **kwargs)
            
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send Slack alert: {str(e)}")
            return False

    def send_pagerduty_alert(self, level: str, message: str, alert_type: str = 'system', **kwargs) -> bool:
        """Send alert to PagerDuty with formatted message"""
        try:
            if not (self.pagerduty_config['api_key'] and self.pagerduty_config['service_id']):
                return False
                
            severity = {
                'INFO': 'info',
                'WARNING': 'warning',
                'CRITICAL': 'critical'
            }.get(level, 'info')
            
            formatted = self._format_alert_message(alert_type, level, message, **kwargs)
            
            payload = {
                'incident': {
                    'type': 'incident',
                    'title': f"QDT {self.alert_templates[alert_type]['title']} - {level}",
                    'body': {
                        'type': 'incident_body',
                        'details': formatted['plain_text']
                    },
                    'service': {
                        'id': self.pagerduty_config['service_id'],
                        'type': 'service_reference'
                    },
                    'priority': {
                        'type': 'priority_reference',
                        'id': 'P1' if level == 'CRITICAL' else 'P2'
                    },
                    'urgency': 'high' if level == 'CRITICAL' else 'low',
                    'incident_key': f"qdt-{alert_type}-{int(time.time())}"
                }
            }
            
            headers = {
                'Authorization': f"Token token={self.pagerduty_config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://api.pagerduty.com/incidents',
                json=payload,
                headers=headers
            )
            
            if response.status_code == 201:
                self._record_alert(alert_type, level, message, **kwargs)
            
            return response.status_code == 201
        except Exception as e:
            print(f"Failed to send PagerDuty alert: {str(e)}")
            return False

    def send_alert(self, level: str, message: str, alert_type: str = 'system', **kwargs) -> Dict[str, bool]:
        """Send alerts through all configured channels with formatted messages"""
        results = {
            'email': self.send_email_alert(level, message, alert_type, **kwargs),
            'slack': self.send_slack_alert(level, message, alert_type, **kwargs),
            'pagerduty': self.send_pagerduty_alert(level, message, alert_type, **kwargs)
        }
        return results

    def get_alert_history(self, limit: int = 100) -> List[Dict]:
        """Get recent alert history"""
        return self._alert_history[-limit:]

    def get_alert_summary(self) -> Dict:
        """Get a summary of recent alerts"""
        if not self._alert_history:
            return {'total': 0, 'by_level': {}, 'by_type': {}}
            
        summary = {
            'total': len(self._alert_history),
            'by_level': {},
            'by_type': {}
        }
        
        for alert in self._alert_history:
            summary['by_level'][alert['level']] = summary['by_level'].get(alert['level'], 0) + 1
            summary['by_type'][alert['type']] = summary['by_type'].get(alert['type'], 0) + 1
            
        return summary 