"""Flask API for Crystal Calculator QDT Module."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ..physics.crystal_calculator import CrystalCalculator, CrystalCalculatorConfig
from typing import Dict, Any
import time

app = Flask(__name__)
CORS(app)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

def validate_request_data(data: Dict[str, Any], required_fields: list) -> tuple[bool, str]:
    """Validate request data contains required fields."""
    if not data or not isinstance(data, dict):
        return False, "Invalid request data"
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, ""

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
        
        config = CrystalCalculatorConfig(
            evolution_steps=evolution_steps,
            convergence_threshold=0.01,
            stability_window=10,
            resonance_depth=5
        )
        
        calculator = CrystalCalculator(config=config)
        result = calculator.calculate_crystal_enhanced_value(value, calculation_type)
        
        return jsonify(result)
    except ValueError as e:
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
        
        # Initialize calculator with default config
        calculator = CrystalCalculator()
        
        # Generate a sample calculation to analyze patterns
        sample_result = calculator.calculate_crystal_enhanced_value(1.0, 'currency')
        
        # Analyze convergence patterns
        convergence_analysis = calculator.analyze_convergence_path(sample_result['time_series'])
        
        # Generate response based on crystal patterns
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
    app.run(debug=True, port=5000) 