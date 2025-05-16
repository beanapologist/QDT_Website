"""Crystal Calculator QDT Module

This module integrates time crystal dynamics with the QDT calculator
to measure convergence and progress towards true value realization.

Mathematical Domain:
- Perfect oscillations
- Exact convergence
- Clean resonance patterns

Physical Reality:
- Quantum fluctuations
- Convergence uncertainty
- Complex interactions
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from .time_crystal import TimeCrystalOscillator, TimeCrystalParameters
from .constants import QDTConstants

@dataclass
class CrystalCalculatorConfig:
    """Configuration for crystal-enhanced calculations."""
    evolution_steps: int = 100
    convergence_threshold: float = 0.01
    stability_window: int = 10
    resonance_depth: int = 5

class CrystalCalculator:
    """Integrates time crystal dynamics with QDT value calculations."""
    
    def __init__(self, 
                 config: Optional[CrystalCalculatorConfig] = None,
                 crystal_params: Optional[TimeCrystalParameters] = None):
        """Initialize crystal calculator with QDT coupling."""
        self.config = config or CrystalCalculatorConfig()
        self.crystal = TimeCrystalOscillator(crystal_params=crystal_params)
        self.constants = self.crystal.constants

    def calculate_crystal_enhanced_value(self, 
                                       value: float, 
                                       calculation_type: str) -> Dict:
        """Calculate QDT value with time crystal enhancement.
        
        Mathematical Domain:
        - Perfect value convergence
        - Exact type mapping
        - Clean evolution path
        
        Physical Reality:
        - Value uncertainty
        - Type ambiguity
        - Complex dynamics
        """
        # Type-specific multipliers
        type_multipliers = {
            'currency': 0.867,
            'human_life': 1.618,
            'natural_resource': 1.414,
            'crypto': 0.618,
            'art': 1.732,
            'radioactive_potato': np.pi
        }
        multiplier = type_multipliers.get(calculation_type, 1.0)
        
        # Initialize evolution tracking
        time_series = {
            'void': [],
            'filament': [],
            'emergence': [],
            'resonance': [],
            'crystal_phase': [],
            'convergence': []
        }
        
        # Generate time steps
        time_steps = np.linspace(0, 10, self.config.evolution_steps)
        
        # Track convergence metrics
        convergence_history = []
        stability_window = []
        
        for t in time_steps:
            # Calculate crystal modulation
            crystal_mod = self.crystal.time_crystal_modulation(t)
            
            # Base void energy with crystal coupling
            void_energy = np.exp(-self.constants.GAMMA * t) * \
                         (1/np.max([1, t]))**self.constants.BETA * \
                         (1 + 0.1 * crystal_mod)
            
            # Emergence energy with crystal stability
            emergence_energy = self.constants.ETA * \
                             (1 - np.exp(-0.1 * t)) * \
                             np.sin(np.pi * t * self.constants.PHI) * \
                             self.constants.LAMBDA * \
                             self.constants.GAMMA * \
                             (1 + 0.05 * crystal_mod)
            
            # Calculate prime resonances with crystal phase
            resonances = []
            for i in range(self.config.resonance_depth):
                p = self._get_prime(i)
                resonance = np.sin(2 * np.pi * p * self.constants.LAMBDA * t) * \
                           np.cos(np.pi * p * self.constants.BETA * t) * \
                           (1 + 0.1 * crystal_mod)
                resonances.append(resonance)
            
            # Normalize resonances
            total_resonance = np.sum(np.abs(resonances))
            if total_resonance > 0:
                normalized_resonance = np.sum(resonances) / total_resonance
            else:
                normalized_resonance = 0
            
            # Filament energy with crystal-enhanced coupling
            filament_energy = self.constants.LAMBDA * (1 - void_energy) + \
                            normalized_resonance * \
                            (void_energy + emergence_energy)/2 * \
                            (1 + 0.1 * crystal_mod)
            
            # Normalize energies
            total = void_energy + filament_energy + emergence_energy
            void_energy /= total
            filament_energy /= total
            emergence_energy /= total
            
            # Calculate convergence metric
            crystal_phase = self.crystal.time_crystal_oscillation(t)
            convergence = np.abs(crystal_phase - normalized_resonance)
            
            # Update stability window
            stability_window.append(convergence)
            if len(stability_window) > self.config.stability_window:
                stability_window.pop(0)
            
            # Track metrics
            time_series['void'].append(void_energy)
            time_series['filament'].append(filament_energy)
            time_series['emergence'].append(emergence_energy)
            time_series['resonance'].append(normalized_resonance)
            time_series['crystal_phase'].append(crystal_phase)
            time_series['convergence'].append(convergence)
            
            convergence_history.append(np.mean(stability_window))
        
        # Calculate final QDT value
        final_void = time_series['void'][-1]
        final_filament = time_series['filament'][-1]
        final_emergence = time_series['emergence'][-1]
        
        qdt_value = value * multiplier * (
            final_void * 0.4 + 
            final_filament * 0.4 + 
            final_emergence * 0.2
        )
        
        # Calculate convergence metrics
        stability_score = 1 - np.mean(convergence_history[-self.config.stability_window:])
        convergence_rate = np.mean(np.diff(convergence_history))
        final_convergence = convergence_history[-1]
        
        # Analyze crystal stability
        crystal_stability = self.crystal.analyze_crystal_stability(
            t_max=10.0, 
            n_steps=self.config.evolution_steps
        )
        
        return {
            'original_value': value,
            'qdt_value': qdt_value,
            'void_energy': final_void,
            'filament_energy': final_filament,
            'emergence_energy': final_emergence,
            'time_series': time_series,
            'convergence_metrics': {
                'stability_score': stability_score,
                'convergence_rate': convergence_rate,
                'final_convergence': final_convergence,
                'phase_coherence': crystal_stability['phase_coherence'],
                'amplitude_stability': crystal_stability['amplitude_stability']
            }
        }

    def _get_prime(self, n: int) -> int:
        """Get nth prime number."""
        primes = []
        num = 2
        while len(primes) <= n:
            if all(num % prime != 0 for prime in primes):
                primes.append(num)
            num += 1
        return primes[-1]

    def analyze_convergence_path(self, 
                               time_series: Dict[str, List[float]]) -> Dict:
        """Analyze the convergence path through crystal dynamics.
        
        Mathematical Domain:
        - Perfect trajectory analysis
        - Exact convergence metrics
        - Clean phase relationships
        
        Physical Reality:
        - Path uncertainty
        - Metric fluctuations
        - Complex phase dynamics
        """
        # Calculate phase space metrics
        void_filament_coupling = np.corrcoef(
            time_series['void'], 
            time_series['filament']
        )[0, 1]
        
        crystal_resonance_coupling = np.corrcoef(
            time_series['crystal_phase'], 
            time_series['resonance']
        )[0, 1]
        
        # Analyze convergence stability
        convergence_stability = 1 - np.std(time_series['convergence'])
        
        # Calculate effective dimensionality
        components = [
            time_series['void'],
            time_series['filament'],
            time_series['emergence'],
            time_series['crystal_phase']
        ]
        correlations = np.corrcoef(components)
        eigenvalues = np.linalg.eigvals(correlations)
        effective_dim = np.sum(eigenvalues > 0.1)  # 10% threshold
        
        return {
            'void_filament_coupling': void_filament_coupling,
            'crystal_resonance_coupling': crystal_resonance_coupling,
            'convergence_stability': convergence_stability,
            'effective_dimensionality': effective_dim,
            'final_convergence': time_series['convergence'][-1]
        } 