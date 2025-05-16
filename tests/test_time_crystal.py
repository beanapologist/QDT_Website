"""Tests for the Time Crystal QDT module."""

import numpy as np
import pytest
from src.physics.time_crystal import TimeCrystalOscillator, TimeCrystalParameters
from src.physics.constants import QDTConstants

def test_time_crystal_initialization():
    """Test time crystal oscillator initialization."""
    oscillator = TimeCrystalOscillator()
    assert isinstance(oscillator.constants, QDTConstants)
    assert isinstance(oscillator.params, TimeCrystalParameters)
    assert oscillator.time_offset == 0
    assert not oscillator.phase_lock

def test_basic_oscillation():
    """Test basic time crystal oscillation."""
    oscillator = TimeCrystalOscillator()
    t = np.linspace(0, 10, 1000)
    
    # Test with default parameters
    oscillations = np.array([oscillator.time_crystal_oscillation(ti) for ti in t])
    assert len(oscillations) == len(t)
    assert np.all(np.abs(oscillations) <= oscillator.params.CRYSTAL_AMPLITUDE)
    
    # Test with custom parameters
    custom_freq = 2.0
    custom_amp = 0.2
    custom_oscillations = np.array([
        oscillator.time_crystal_oscillation(ti, custom_freq, custom_amp) 
        for ti in t
    ])
    assert len(custom_oscillations) == len(t)
    assert np.all(np.abs(custom_oscillations) <= custom_amp)

def test_time_crystal_modulation():
    """Test QDT-enhanced time crystal modulation."""
    oscillator = TimeCrystalOscillator()
    steps = np.linspace(0, 100, 1000)
    
    modulations = np.array([oscillator.time_crystal_modulation(step) for step in steps])
    assert len(modulations) == len(steps)
    
    # Test damping effect
    assert np.abs(modulations[-1]) < np.abs(modulations[0])

def test_time_evolution_crystalized():
    """Test field evolution with time crystal stability."""
    oscillator = TimeCrystalOscillator()
    
    # Create test fields
    fields = {
        'field1': [1.0, 2.0, 3.0],
        'field2': [0.5, 1.5, 2.5]
    }
    
    # Evolve fields
    evolved_fields = oscillator.time_evolution_crystalized(fields.copy(), time_step=1.0)
    
    # Check structure preservation
    assert set(evolved_fields.keys()) == set(fields.keys())
    assert all(len(evolved_fields[key]) == len(fields[key]) for key in fields)
    
    # Check evolution effects
    for key in fields:
        assert not np.array_equal(evolved_fields[key], fields[key])

def test_crystal_stability_analysis():
    """Test time crystal stability analysis."""
    oscillator = TimeCrystalOscillator()
    
    # Run stability analysis
    results = oscillator.analyze_crystal_stability(t_max=10.0, n_steps=1000)
    
    # Check results structure
    expected_keys = {'time', 'oscillations', 'modulations', 
                    'phase_coherence', 'amplitude_stability'}
    assert set(results.keys()) == expected_keys
    
    # Check array shapes
    assert len(results['time']) == 1000
    assert len(results['oscillations']) == 1000
    assert len(results['modulations']) == 1000
    
    # Check stability metrics
    assert 0 <= results['phase_coherence'] <= 1
    assert results['amplitude_stability'] > 0

def test_parameter_bounds():
    """Test time crystal parameter bounds and effects."""
    params = TimeCrystalParameters(
        CRYSTAL_FREQUENCY=2.0,
        CRYSTAL_AMPLITUDE=0.2,
        GAMMA_T=0.3
    )
    oscillator = TimeCrystalOscillator(crystal_params=params)
    
    t = np.linspace(0, 10, 1000)
    oscillations = np.array([oscillator.time_crystal_oscillation(ti) for ti in t])
    
    # Check frequency effects
    fft_freqs = np.fft.fftfreq(len(t), t[1] - t[0])
    fft_vals = np.abs(np.fft.fft(oscillations))
    peak_freq = np.abs(fft_freqs[np.argmax(fft_vals[1:])+1])
    assert np.abs(peak_freq - params.CRYSTAL_FREQUENCY) < 0.1
    
    # Check amplitude bounds
    assert np.all(np.abs(oscillations) <= params.CRYSTAL_AMPLITUDE)

def test_energy_conservation():
    """Test energy conservation in time crystal evolution."""
    oscillator = TimeCrystalOscillator()
    
    # Create test fields with unit energy
    fields = {
        'energy': [1.0, 1.0, 1.0]
    }
    
    # Evolve multiple steps
    current_fields = fields.copy()
    energies = []
    
    for t in range(10):
        current_fields = oscillator.time_evolution_crystalized(current_fields, t)
        total_energy = sum(sum(field) for field in current_fields.values())
        energies.append(total_energy)
    
    # Check energy variation is bounded
    energy_variation = np.std(energies) / np.mean(energies)
    assert energy_variation < 0.1  # 10% variation tolerance 