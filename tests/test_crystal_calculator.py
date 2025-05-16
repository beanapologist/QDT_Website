"""Tests for the Crystal Calculator QDT module."""

import numpy as np
import pytest
from src.physics.crystal_calculator import CrystalCalculator, CrystalCalculatorConfig
from src.physics.time_crystal import TimeCrystalParameters

def test_crystal_calculator_initialization():
    """Test crystal calculator initialization."""
    calculator = CrystalCalculator()
    assert calculator.config.evolution_steps == 100
    assert calculator.config.convergence_threshold == 0.01
    assert calculator.config.stability_window == 10
    assert calculator.config.resonance_depth == 5

def test_custom_configuration():
    """Test crystal calculator with custom configuration."""
    config = CrystalCalculatorConfig(
        evolution_steps=200,
        convergence_threshold=0.005,
        stability_window=20,
        resonance_depth=10
    )
    calculator = CrystalCalculator(config=config)
    assert calculator.config.evolution_steps == 200
    assert calculator.config.convergence_threshold == 0.005
    assert calculator.config.stability_window == 20
    assert calculator.config.resonance_depth == 10

def test_value_calculation():
    """Test QDT value calculation with crystal enhancement."""
    calculator = CrystalCalculator()
    
    # Test with currency type
    result = calculator.calculate_crystal_enhanced_value(100.0, 'currency')
    assert isinstance(result, dict)
    assert 'original_value' in result
    assert 'qdt_value' in result
    assert 'convergence_metrics' in result
    assert result['original_value'] == 100.0
    assert 0 < result['qdt_value'] < 100.0  # Should be reduced by multiplier

def test_time_series_structure():
    """Test time series data structure."""
    calculator = CrystalCalculator()
    result = calculator.calculate_crystal_enhanced_value(100.0, 'currency')
    
    expected_keys = {'void', 'filament', 'emergence', 
                    'resonance', 'crystal_phase', 'convergence'}
    assert set(result['time_series'].keys()) == expected_keys
    
    # Check array lengths
    n_steps = calculator.config.evolution_steps
    for key in expected_keys:
        assert len(result['time_series'][key]) == n_steps

def test_convergence_metrics():
    """Test convergence metrics calculation."""
    calculator = CrystalCalculator()
    result = calculator.calculate_crystal_enhanced_value(100.0, 'currency')
    
    metrics = result['convergence_metrics']
    expected_metrics = {'stability_score', 'convergence_rate', 
                       'final_convergence', 'phase_coherence', 
                       'amplitude_stability'}
    assert set(metrics.keys()) == expected_metrics
    
    # Check metric bounds
    assert 0 <= metrics['stability_score'] <= 1
    assert -1 <= metrics['convergence_rate'] <= 1
    assert 0 <= metrics['phase_coherence'] <= 1
    assert metrics['amplitude_stability'] > 0

def test_energy_conservation():
    """Test energy conservation in calculations."""
    calculator = CrystalCalculator()
    result = calculator.calculate_crystal_enhanced_value(100.0, 'currency')
    
    # Check energy normalization
    void = result['void_energy']
    filament = result['filament_energy']
    emergence = result['emergence_energy']
    
    total = void + filament + emergence
    assert np.abs(total - 1.0) < 1e-10  # Should sum to 1 within numerical precision

def test_convergence_path_analysis():
    """Test convergence path analysis."""
    calculator = CrystalCalculator()
    result = calculator.calculate_crystal_enhanced_value(100.0, 'currency')
    
    path_analysis = calculator.analyze_convergence_path(result['time_series'])
    expected_metrics = {'void_filament_coupling', 'crystal_resonance_coupling',
                       'convergence_stability', 'effective_dimensionality',
                       'final_convergence'}
    assert set(path_analysis.keys()) == expected_metrics
    
    # Check metric bounds
    assert -1 <= path_analysis['void_filament_coupling'] <= 1
    assert -1 <= path_analysis['crystal_resonance_coupling'] <= 1
    assert 0 <= path_analysis['convergence_stability'] <= 1
    assert 1 <= path_analysis['effective_dimensionality'] <= 4

def test_different_calculation_types():
    """Test different calculation types."""
    calculator = CrystalCalculator()
    types = ['currency', 'human_life', 'natural_resource', 
             'crypto', 'art', 'radioactive_potato']
    
    base_value = 100.0
    results = {}
    
    for calc_type in types:
        result = calculator.calculate_crystal_enhanced_value(base_value, calc_type)
        results[calc_type] = result['qdt_value']
    
    # Each type should give different results
    values = list(results.values())
    assert len(set(values)) == len(types)  # All values should be unique

def test_crystal_stability():
    """Test crystal stability analysis."""
    calculator = CrystalCalculator()
    result = calculator.calculate_crystal_enhanced_value(100.0, 'currency')
    
    # Check stability metrics
    metrics = result['convergence_metrics']
    assert metrics['stability_score'] > 0  # Should have some stability
    assert metrics['phase_coherence'] > 0  # Should maintain some coherence
    
    # Evolution should show convergence
    convergence = result['time_series']['convergence']
    assert convergence[-1] < convergence[0]  # Should improve over time 