from flask import Blueprint, render_template, jsonify, request, current_app
from src.security.monitoring import SecurityMonitor
from src.security.metrics import SecurityMetrics
import json
import logging

dashboard = Blueprint('security_dashboard', __name__)
metrics = SecurityMetrics()

@dashboard.route('/security/dashboard')
def show_dashboard():
    """Render the security dashboard"""
    return render_template('security/dashboard.html')

@dashboard.route('/security/metrics')
def get_metrics():
    """Get current security metrics"""
    return jsonify({
        'security_events': metrics.get_security_events(),
        'system_metrics': metrics.get_system_metrics(),
        'alerts': metrics.get_alerts()
    })

@dashboard.route('/security/events')
def get_events():
    """Get recent security events"""
    events = metrics.get_security_events(limit=100)
    return jsonify(events)

@dashboard.route('/accessibility')
def accessibility_guide():
    """Render the accessibility documentation page"""
    return render_template('accessibility.html')

@dashboard.route('/accessibility/feedback')
def accessibility_feedback():
    """Render the accessibility feedback form"""
    return render_template('accessibility_feedback.html')

@dashboard.route('/accessibility/feedback', methods=['POST'])
def submit_accessibility_feedback():
    """Handle accessibility feedback submissions"""
    try:
        feedback_data = {
            'type': request.form.get('feedback_type'),
            'area': request.form.get('feedback_area'),
            'description': request.form.get('feedback_description'),
            'impact_level': request.form.get('impact_level'),
            'assistive_technology': request.form.get('assistive_technology'),
            'contact_email': request.form.get('contact_email')
        }
        
        # Log the feedback
        current_app.logger.info('Accessibility Feedback Received: %s', json.dumps(feedback_data))
        
        # Here you would typically store the feedback in a database
        # For now, we'll just return a success response
        
        return jsonify({'status': 'success', 'message': 'Feedback received successfully'}), 200
    except Exception as e:
        current_app.logger.error('Error processing accessibility feedback: %s', str(e))
        return jsonify({'status': 'error', 'message': 'Failed to process feedback'}), 500 