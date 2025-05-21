"""Flask API for Crystal Calculator QDT Module."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
from physics.crystal_calculator import CrystalCalculator, CrystalCalculatorConfig
from typing import Dict, Any
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Production configurations
app.config['PRODUCTION'] = os.getenv('FLASK_ENV') == 'production'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Configure Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Quantum Duality Theory API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"],
    storage_uri=app.config['REDIS_URL']
)

def validate_request_data(data: Dict[str, Any], required_fields: list) -> tuple[bool, str]:
    """Validate request data contains required fields."""
    if not data or not isinstance(data, dict):
        return False, "Invalid request data"
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, ""

@app.route('/api/swagger.json')
def swagger():
    """Serve the swagger specification."""
    with open('src/api/swagger.json', 'r') as f:
        return jsonify(json.load(f))

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0.0'
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current calculator configuration."""
    config = CrystalCalculatorConfig()
    return jsonify({
        'evolution_steps': config.evolution_steps,
        'convergence_threshold': config.convergence_threshold,
        'stability_window': config.stability_window,
        'resonance_depth': config.resonance_depth
    })

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    return jsonify(error="Rate limit exceeded. Please try again later."), 429

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle general exceptions."""
    app.logger.error(f"Error processing request: {str(e)}")
    return jsonify(error="An internal error occurred. Please try again."), 500

@app.route('/api/calculate', methods=['POST'])
@limiter.limit("30 per minute")
def calculate():
    """Calculate QDT value with crystal enhancement."""
    try:
        data = request.json
        valid, error_msg = validate_request_data(data, ['value', 'calculation_type'])
        if not valid:
            return jsonify(error=error_msg), 400
        
        value = float(data['value'])
        calculation_type = data['calculation_type']
        evolution_steps = int(data.get('evolution_steps', 100))
        
        if evolution_steps < 10 or evolution_steps > 1000:
            return jsonify(error="Evolution steps must be between 10 and 1000"), 400
        
        # Validate calculation type
        valid_types = ['currency', 'energy', 'probability']
        if calculation_type not in valid_types:
            return jsonify(error=f"Invalid calculation type. Must be one of: {', '.join(valid_types)}"), 400
        
        # Validate input value
        if value <= 0:
            return jsonify(error="Value must be greater than 0"), 400
        
        config = CrystalCalculatorConfig(
            evolution_steps=evolution_steps,
            convergence_threshold=0.01,
            stability_window=10,
            resonance_depth=5
        )
        
        calculator = CrystalCalculator(config=config)
        result = calculator.calculate_crystal_enhanced_value(value, calculation_type)
        
        # Ensure time series data is properly structured and optimized
        time_series = {
            'void_energy': [float(x) for x in result['time_series']['void_energy']],
            'filament_energy': [float(x) for x in result['time_series']['filament_energy']],
            'emergence_energy': [float(x) for x in result['time_series']['emergence_energy']],
            'crystal_phase': [float(x) for x in result['time_series']['crystal_phase']],
            'resonance': [float(x) for x in result['time_series']['resonance']],
            'steps': list(range(1, len(result['time_series']['void_energy']) + 1))
        }
        
        response = {
            'void_energy': float(result['void_energy']),
            'filament_energy': float(result['filament_energy']),
            'emergence_energy': float(result['emergence_energy']),
            'crystal_phase': float(result['crystal_phase']),
            'resonance': float(result['resonance']),
            'convergence_metrics': {
                'stability_score': float(result['convergence_metrics']['stability_score']),
                'phase_coherence': float(result['convergence_metrics']['phase_coherence']),
                'convergence_rate': float(result['convergence_metrics']['convergence_rate'])
            },
            'time_series': time_series
        }
        
        # Add cache control headers
        response_headers = {
            'Cache-Control': 'public, max-age=300',  # Cache for 5 minutes
            'Vary': 'Accept-Encoding'
        }
        
        return jsonify(response), 200, response_headers
    except ValueError as e:
        app.logger.error(f"Value error in calculate: {str(e)}")
        return jsonify(error=f"Invalid input: {str(e)}"), 400
    except Exception as e:
        app.logger.error(f"Error in calculate: {str(e)}")
        return jsonify(error="Failed to process calculation"), 500

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("30 per minute")
def analyze():
    """Analyze convergence path."""
    try:
        data = request.json
        valid, error_msg = validate_request_data(data, ['time_series'])
        if not valid:
            return jsonify(error=error_msg), 400
        
        time_series = data['time_series']
        
        calculator = CrystalCalculator()
        result = calculator.analyze_convergence_path(time_series)
        
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in analyze: {str(e)}")
        return jsonify(error="Failed to analyze convergence path"), 500

@app.route('/api/batch', methods=['POST'])
@limiter.limit("10 per minute")
def batch_calculate():
    """Perform batch calculations."""
    try:
        data = request.json
        valid, error_msg = validate_request_data(data, ['calculations'])
        if not valid:
            return jsonify(error=error_msg), 400
        
        calculations = data['calculations']
        if not isinstance(calculations, list):
            return jsonify(error="Calculations must be a list"), 400
        
        if len(calculations) > 10:
            return jsonify(error="Maximum 10 calculations per batch"), 400
        
        calculator = CrystalCalculator()
        results = []
        
        for calc in calculations:
            try:
                valid, error_msg = validate_request_data(calc, ['value', 'calculation_type'])
                if not valid:
                    results.append({'error': error_msg})
                    continue
                
                result = calculator.calculate_crystal_enhanced_value(
                    float(calc['value']), 
                    calc['calculation_type']
                )
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        
        return jsonify({'results': results})
    except Exception as e:
        app.logger.error(f"Error in batch calculate: {str(e)}")
        return jsonify(error="Failed to process batch calculation"), 500

@app.route('/api/ask', methods=['POST'])
@limiter.limit("20 per minute")
def ask():
    """Handle QDT-related questions using crystal calculator analysis."""
    try:
        start_time = time.time()
        
        data = request.json
        valid, error_msg = validate_request_data(data, ['question'])
        if not valid:
            return jsonify(error=error_msg), 400
        
        question = data['question']
        if not isinstance(question, str) or len(question.strip()) < 3:
            return jsonify(error="Question must be at least 3 characters long"), 400
        
        calculator = CrystalCalculator()
        sample_result = calculator.calculate_crystal_enhanced_value(1.0, 'currency')
        convergence_analysis = calculator.analyze_convergence_path(sample_result['time_series'])
        
        response = {
            'answer': generate_qdt_response(
                question, 
                sample_result, 
                convergence_analysis
            ),
            'confidence': calculate_response_confidence(convergence_analysis),
            'crystal_metrics': {
                'phase_coherence': sample_result['convergence_metrics']['phase_coherence'],
                'stability': sample_result['convergence_metrics']['stability_score'],
                'resonance': convergence_analysis['crystal_resonance_coupling']
            },
            'processing_time': time.time() - start_time
        }
        
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in ask: {str(e)}")
        return jsonify(error="Failed to process question"), 500

def generate_qdt_response(question: str, 
                        calculation_result: dict, 
                        convergence_analysis: dict) -> str:
    """Generate a response based on crystal patterns and QDT analysis."""
    # Extract key metrics
    stability = calculation_result['convergence_metrics']['stability_score']
    coherence = calculation_result['convergence_metrics']['phase_coherence']
    resonance = convergence_analysis['crystal_resonance_coupling']
    
    # Basic response templates
    if stability > 0.8:
        base_response = "With high stability in the crystal phase, "
    elif stability > 0.5:
        base_response = "Based on moderate crystal stability, "
    else:
        base_response = "Given the current quantum fluctuations, "
    
    # Add coherence analysis
    if coherence > 0.7:
        base_response += "and strong phase coherence, "
    else:
        base_response += "and varying phase relationships, "
    
    # Add resonance insight
    if resonance > 0.6:
        base_response += "the quantum resonance patterns suggest "
    else:
        base_response += "the emerging patterns indicate "
    
    # Question-specific responses
    if "convergence" in question.lower():
        return base_response + f"a convergence rate of {calculation_result['convergence_metrics']['convergence_rate']:.2%} per step."
    elif "stability" in question.lower():
        return base_response + f"a crystal stability score of {stability:.2%}."
    elif "energy" in question.lower():
        return base_response + f"void energy at {calculation_result['void_energy']:.2%} and filament energy at {calculation_result['filament_energy']:.2%}."
    else:
        return base_response + "a complex interplay of quantum duality factors affecting the system."

def calculate_response_confidence(convergence_analysis: dict) -> float:
    """Calculate confidence score for the response."""
    return min(1.0, max(0.0, 
        convergence_analysis['convergence_stability'] * 0.4 +
        abs(convergence_analysis['crystal_resonance_coupling']) * 0.3 +
        (1 - abs(convergence_analysis['void_filament_coupling'])) * 0.3
    ))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=not app.config['PRODUCTION']) 