import type { 
  CrystalCalculator, 
  CrystalCalculationResult,
  QDTResponse 
} from '../types/crystal_calculator';

const API_BASE_URL = 'http://localhost:5000/api';

export class CrystalCalculatorService implements CrystalCalculator {
  async calculate_crystal_enhanced_value(
    value: number,
    calculation_type: string,
    evolution_steps: number = 100
  ): Promise<CrystalCalculationResult> {
    const response = await fetch(`${API_BASE_URL}/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        value,
        calculation_type,
        evolution_steps,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to calculate crystal-enhanced value');
    }

    return response.json();
  }

  async analyze_convergence_path(
    time_series: {
      void: number[];
      filament: number[];
      emergence: number[];
      resonance: number[];
      crystal_phase: number[];
      convergence: number[];
    }
  ): Promise<{
    void_filament_coupling: number;
    crystal_resonance_coupling: number;
    convergence_stability: number;
    effective_dimensionality: number;
    final_convergence: number;
  }> {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ time_series }),
    });

    if (!response.ok) {
      throw new Error('Failed to analyze convergence path');
    }

    return response.json();
  }

  async ask(question: string): Promise<QDTResponse> {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error('Failed to process QDT question');
    }

    return response.json();
  }
}

// Create a singleton instance
export const crystalCalculator = new CrystalCalculatorService(); 