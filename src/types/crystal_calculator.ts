export interface TimeCrystalParameters {
  CRYSTAL_FREQUENCY: number;
  CRYSTAL_AMPLITUDE: number;
  GAMMA_T: number;
}

export interface CrystalCalculatorConfig {
  evolution_steps: number;
  convergence_threshold: number;
  stability_window: number;
  resonance_depth: number;
}

export interface CrystalCalculationResult {
  original_value: number;
  qdt_value: number;
  void_energy: number;
  filament_energy: number;
  emergence_energy: number;
  time_series: {
    void: number[];
    filament: number[];
    emergence: number[];
    resonance: number[];
    crystal_phase: number[];
    convergence: number[];
  };
  convergence_metrics: {
    stability_score: number;
    convergence_rate: number;
    final_convergence: number;
    phase_coherence: number;
    amplitude_stability: number;
  };
}

export interface ConvergenceAnalysisResult {
  void_filament_coupling: number;
  crystal_resonance_coupling: number;
  convergence_stability: number;
  effective_dimensionality: number;
  final_convergence: number;
}

export interface QDTResponse {
  answer: string;
  confidence: number;
  crystal_metrics: {
    phase_coherence: number;
    stability: number;
    resonance: number;
  };
}

export interface CrystalCalculator {
  calculate_crystal_enhanced_value(
    value: number, 
    calculation_type: string,
    evolution_steps?: number
  ): Promise<CrystalCalculationResult>;
  
  analyze_convergence_path(
    time_series: {
      void: number[];
      filament: number[];
      emergence: number[];
      resonance: number[];
      crystal_phase: number[];
      convergence: number[];
    }
  ): Promise<ConvergenceAnalysisResult>;

  ask(question: string): Promise<QDTResponse>;
} 